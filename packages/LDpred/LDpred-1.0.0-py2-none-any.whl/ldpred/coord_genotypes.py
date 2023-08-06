#!/usr/bin/env python

import os
import scipy as sp
import gzip
import h5py
from ldpred import sum_stats_parsers
from ldpred import util
from ldpred import plinkfiles




def _verify_coord_data_(data_dict):
    """
    Verify that merged data is ok
    """
    num_snps = len(data_dict['raw_snps_ref'])
    assert num_snps ==len(data_dict['snp_stds_ref']), 'Inconsistencies in coordinated data sizes'
    assert num_snps ==len(data_dict['snp_means_ref']), 'Inconsistencies in coordinated data sizes'
    assert num_snps ==len(data_dict['freqs_ref']), 'Inconsistencies in coordinated data sizes'
    assert num_snps ==len(data_dict['ps']), 'Inconsistencies in coordinated data sizes'
    assert num_snps ==len(data_dict['positions']), 'Inconsistencies in coordinated data sizes'
    assert num_snps ==len(data_dict['nts']), 'Inconsistencies in coordinated data sizes'
    assert num_snps ==len(data_dict['sids']), 'Inconsistencies in coordinated data sizes'
    assert num_snps ==len(data_dict['betas']), 'Inconsistencies in coordinated data sizes'
    assert num_snps ==len(data_dict['log_odds']), 'Inconsistencies in coordinated data sizes'
    if 'raw_snps_val' in data_dict:
        assert num_snps ==len(data_dict['raw_snps_val']), 'Inconsistencies in coordinated data sizes'
        assert num_snps ==len(data_dict['snp_stds_val']), 'Inconsistencies in coordinated data sizes'
        assert num_snps ==len(data_dict['snp_means_val']), 'Inconsistencies in coordinated data sizes'
        assert num_snps ==len(data_dict['freqs_val']), 'Inconsistencies in coordinated data sizes'
    


def write_coord_data(cord_data_g, coord_dict):
    _verify_coord_data_(coord_dict)
    print('Storing coordinated data to HDF5 file.')
    ofg = cord_data_g.create_group(coord_dict['chrom'])
    ofg.create_dataset('raw_snps_ref', data=coord_dict['raw_snps_ref'], compression='lzf')
    ofg.create_dataset('snp_stds_ref', data=coord_dict['snp_stds_ref'])
    ofg.create_dataset('snp_means_ref', data=coord_dict['snp_means_ref'])
    ofg.create_dataset('freqs_ref', data=coord_dict['freqs_ref'])
    if 'raw_snps_val' in coord_dict:
        ofg.create_dataset('raw_snps_val', data=coord_dict['raw_snps_val'], compression='lzf')
        ofg.create_dataset('snp_stds_val', data=coord_dict['snp_stds_val'])
        ofg.create_dataset('snp_means_val', data=coord_dict['snp_means_val'])
        ofg.create_dataset('freqs_val', data=coord_dict['freqs_val'])
    
    ofg.create_dataset('ps', data=coord_dict['ps'])
    ofg.create_dataset('positions', data=coord_dict['positions'])
    ofg.create_dataset('nts', data=sp.array(coord_dict['nts'],dtype=util.nts_dtype))
    ofg.create_dataset('sids', data=sp.array(coord_dict['sids'],dtype=util.sids_dtype))
    ofg.create_dataset('betas', data=coord_dict['betas'])
    ofg.create_dataset('log_odds', data=coord_dict['log_odds'])
    ofg.create_dataset('log_odds_prs', data=coord_dict['log_odds_prs'])

    if coord_dict['genetic_map'] is not None:
        ofg.create_dataset('genetic_map', data=coord_dict['genetic_map'])



def coordinate_genot_ss(genotype_file=None,
                        hdf5_file=None,
                        genetic_map_dir=None,
                        check_mafs=False,
                        min_maf=0.01,
                        skip_coordination=False,
                        debug=False):
    """
    Assumes plink BED files.  Imputes missing genotypes.
    """
    from plinkio import plinkfile
    plinkf = plinkfile.PlinkFile(genotype_file)
    plinkf_dict = plinkfiles.get_phenotypes(plinkf)
    num_individs = plinkf_dict['num_individs']
    risk_scores = sp.zeros(num_individs)
    rb_risk_scores = sp.zeros(num_individs)
    num_common_snps = 0
    corr_list = []
    rb_corr_list = []

    if plinkf_dict['has_phenotype']:
        hdf5_file.create_dataset('y', data=plinkf_dict['phenotypes'])

    hdf5_file.create_dataset('fids', data=sp.array(plinkf_dict['fids'], dtype=util.fids_dtype))
    hdf5_file.create_dataset('iids', data=sp.array(plinkf_dict['iids'], dtype=util.iids_dtype))
    ssf = hdf5_file['sum_stats']

    cord_data_g = hdf5_file.create_group('cord_data')

    # Figure out chromosomes and positions by looking at SNPs.
    loci = plinkf.get_loci()
    plinkf.close()
    gf_chromosomes = [l.chromosome for l in loci]

    chromosomes = sp.unique(gf_chromosomes)
    chromosomes.sort()
    chr_dict = plinkfiles.get_chrom_dict(loci, chromosomes)

    tot_num_non_matching_nts = 0
    for chrom in chromosomes:
        chr_str = 'chrom_%d' % chrom
        print('Coordinating data for chromosome %s' % chr_str)

        chrom_d = chr_dict[chr_str]
        try:
            ssg = ssf['chrom_%d' % chrom]
        except Exception as err_str:
            print(err_str)
            print('Did not find chromosome in SS dataset.')
            print('Continuing.')
            continue

        g_sids = chrom_d['sids']
        g_sid_set = set(g_sids)
        assert len(g_sid_set) == len(g_sids), 'Some SNPs appear to be duplicated?'
        ss_sids = (ssg['sids'][...]).astype(util.sids_u_dtype)
        ss_sid_set = set(ss_sids)
        assert len(ss_sid_set) == len(ss_sids), 'Some SNPs appear to be duplicated?'

        # Figure out filters:
        g_filter = sp.in1d(g_sids, ss_sids)
        ss_filter = sp.in1d(ss_sids, g_sids)

        # Order by SNP IDs
        g_order = sp.argsort(g_sids)
        ss_order = sp.argsort(ss_sids)

        g_indices = []
        for g_i in g_order:
            if g_filter[g_i]:
                g_indices.append(g_i)

        ss_indices = []
        for ss_i in ss_order:
            if ss_filter[ss_i]:
                ss_indices.append(ss_i)

        g_nts = chrom_d['nts']
        snp_indices = chrom_d['snp_indices']
        ss_nts = (ssg['nts'][...]).astype(util.nts_u_dtype)
        betas = ssg['betas'][...]
        log_odds = ssg['log_odds'][...]
        assert not sp.any(sp.isnan(betas)), 'Some SNP effect estimates are NANs (not a number)'
        assert not sp.any(sp.isinf(betas)), 'Some SNP effect estimates are INFs (infinite numbers)'

        num_non_matching_nts = 0
        num_ambig_nts = 0
        ok_nts = []
        if debug:
            print('Found %d SNPs present in both datasets' % (len(g_indices)))

        if 'freqs' in ssg:
            ss_freqs = ssg['freqs'][...]

        ok_indices = {'g': [], 'ss': []}
        for g_i, ss_i in zip(g_indices, ss_indices):

            # Is the nucleotide ambiguous?
            g_nt = [g_nts[g_i][0], g_nts[g_i][1]]

            if not skip_coordination:
                if tuple(g_nt) in util.ambig_nts:
                    num_ambig_nts += 1
                    tot_num_non_matching_nts += 1
                    continue

                if (not g_nt[0] in util.valid_nts) or (not g_nt[1] in util.valid_nts):
                    num_non_matching_nts += 1
                    tot_num_non_matching_nts += 1
                    continue

                ss_nt = ss_nts[ss_i]

                # Are the nucleotides the same?
                flip_nts = False
                os_g_nt = sp.array(
                    [util.opp_strand_dict[g_nt[0]], util.opp_strand_dict[g_nt[1]]])
                if not (sp.all(g_nt == ss_nt) or sp.all(os_g_nt == ss_nt)):
                    # Opposite strand nucleotides
                    flip_nts = (g_nt[1] == ss_nt[0] and g_nt[0] == ss_nt[1]) or (
                        os_g_nt[1] == ss_nt[0] and os_g_nt[0] == ss_nt[1])
                    if flip_nts:
                        betas[ss_i] = -betas[ss_i]
                        log_odds[ss_i] = -log_odds[ss_i]
                        if 'freqs' in ssg:
                            if ss_freqs[ss_i] > 0:
                                ss_freqs[ss_i] = 1 - ss_freqs[ss_i]
                    else:
                        num_non_matching_nts += 1
                        tot_num_non_matching_nts += 1

                        continue

            # everything seems ok.
            ok_indices['g'].append(g_i)
            ok_indices['ss'].append(ss_i)
            ok_nts.append(g_nt)

        if debug:
            print('%d SNPs were excluded due to ambiguous nucleotides.' % num_ambig_nts)
            print('%d SNPs were excluded due to non-matching nucleotides.' % num_non_matching_nts)

        # Resorting by position
        positions = sp.array(chrom_d['positions'])[ok_indices['g']]
        order = sp.argsort(positions)
        ok_indices['g'] = list(sp.array(ok_indices['g'])[order])
        ok_indices['ss'] = list(sp.array(ok_indices['ss'])[order])
        positions = positions[order]

        # Parse SNPs
        snp_indices = sp.array(chrom_d['snp_indices'])
        
        # Pinpoint where the SNPs are in the file.
        snp_indices = snp_indices[ok_indices['g']]
        raw_snps, freqs = plinkfiles.parse_plink_snps(
            genotype_file, snp_indices)
        if debug:
            print('Parsed a %dX%d (SNP) genotype matrix'%(raw_snps.shape[0],raw_snps.shape[1]))

        snp_stds = sp.sqrt(2 * freqs * (1 - freqs))  
        snp_means = freqs * 2  

        betas = betas[ok_indices['ss']]
        log_odds = log_odds[ok_indices['ss']]
        ps = ssg['ps'][...][ok_indices['ss']]
        nts = sp.array(ok_nts)[order]
        sids = (ssg['sids'][...]).astype(util.sids_u_dtype)
        sids = sids[ok_indices['ss']]

        # Check SNP frequencies..
        if check_mafs and 'freqs' in ssg:
            ss_freqs = ss_freqs[ok_indices['ss']]
            # Assuming freq less than 0 is missing data
            freq_discrepancy_snp = sp.absolute(ss_freqs - (1 - freqs)) > 0.15
            # Filter SNPs that doesn't have MAF info from sumstat
            freq_discrepancy_snp = sp.logical_and(freq_discrepancy_snp, ss_freqs>0)
            freq_discrepancy_snp = sp.logical_and(freq_discrepancy_snp, ss_freqs<1)
            if sp.any(freq_discrepancy_snp):
                print('Warning: %d SNPs appear to have high frequency '
                      'discrepancy between summary statistics and validation sample' %
                      sp.sum(freq_discrepancy_snp))

                # Filter freq_discrepancy_snps
                ok_freq_snps = sp.logical_not(freq_discrepancy_snp)
                raw_snps = raw_snps[ok_freq_snps]
                snp_stds = snp_stds[ok_freq_snps]
                snp_means = snp_means[ok_freq_snps]
                freqs = freqs[ok_freq_snps]
                ps = ps[ok_freq_snps]
                positions = positions[ok_freq_snps]
                nts = nts[ok_freq_snps]
                sids = sids[ok_freq_snps]
                betas = betas[ok_freq_snps]
                log_odds = log_odds[ok_freq_snps]

        # Filter minor allele frequency SNPs.
        maf_filter = (freqs > min_maf) * (freqs < (1 - min_maf))
        maf_filter_sum = sp.sum(maf_filter)
        n_snps = len(maf_filter)
        assert maf_filter_sum <= n_snps, "Problems when filtering SNPs with low minor allele frequencies"
        if sp.sum(maf_filter) < n_snps:
            raw_snps = raw_snps[maf_filter]
            snp_stds = snp_stds[maf_filter]
            snp_means = snp_means[maf_filter]
            freqs = freqs[maf_filter]
            ps = ps[maf_filter]
            positions = positions[maf_filter]
            nts = nts[maf_filter]
            sids = sids[maf_filter]
            betas = betas[maf_filter]
            log_odds = log_odds[maf_filter]

            print('%d SNPs with MAF < %0.3f were filtered' % (n_snps - maf_filter_sum, min_maf))

        print('%d SNPs were retained on chromosome %d.' % (maf_filter_sum, chrom))

        rb_prs = sp.dot(sp.transpose(raw_snps), log_odds)
        if debug and plinkf_dict['has_phenotype']:
            print('Normalizing SNPs')
            snp_means.shape = (len(raw_snps), 1)
            snp_stds.shape = (len(raw_snps), 1)
            snps = (raw_snps - snp_means) / snp_stds
            assert snps.shape == raw_snps.shape, 'Problems when normalizing SNPs (set to have variance 1 and 0 mean)'
            snp_stds = snp_stds.flatten()
            snp_means = snp_means.flatten()
            prs = sp.dot(sp.transpose(snps), betas)
            corr = sp.corrcoef(plinkf_dict['phenotypes'], prs)[0, 1]
            corr_list.append(corr)
            print('PRS correlation for chromosome %d was %0.4f when predicting into LD ref data' % (chrom, corr))
            rb_corr = sp.corrcoef(plinkf_dict['phenotypes'], rb_prs)[0, 1]
            rb_corr_list.append(rb_corr)
            print('Raw effect sizes PRS correlation for chromosome %d was %0.4f when predicting into LD ref data' % (chrom, rb_corr))

        sid_set = set(sids)
        if genetic_map_dir is not None:
            genetic_map = []
            with gzip.open(genetic_map_dir + 'chr%d.interpolated_genetic_map.gz' % chrom) as f:
                for line in f:
                    l = line.split()
                    if l[0] in sid_set:
                        genetic_map.append(l[0])
        else:
            genetic_map = None

        coord_data_dict = {'chrom': 'chrom_%d' % chrom, 
                           'raw_snps_ref': raw_snps, 
                           'snp_stds_ref': snp_stds, 
                           'snp_means_ref': snp_means, 
                           'freqs_ref': freqs,
                           'ps': ps,
                           'positions': positions,
                           'nts': nts,
                           'sids': sids,
                           'genetic_map': genetic_map,
                           'betas': betas,
                           'log_odds': log_odds,
                           'log_odds_prs': rb_prs}
        
        write_coord_data(cord_data_g, coord_data_dict)
        
        if debug and plinkf_dict['has_phenotype']:
            rb_risk_scores += rb_prs
            risk_scores += prs
        num_common_snps += len(betas)

    if debug and plinkf_dict['has_phenotype']:
        
        # Now calculate the prediction R^2
        corr = sp.corrcoef(plinkf_dict['phenotypes'], risk_scores)[0, 1]
        rb_corr = sp.corrcoef(plinkf_dict['phenotypes'], rb_risk_scores)[0, 1]
        print('PRS R2 prediction accuracy for the whole genome was %0.4f (corr=%0.4f) when predicting into LD ref data' % (corr ** 2, corr))
        print('Log-odds (effects) PRS R2 prediction accuracy for the whole genome was %0.4f (corr=%0.4f) when predicting into LD ref data' % (rb_corr ** 2, rb_corr))
    print('There were %d SNPs in common' % num_common_snps)
    print('In all, %d SNPs were excluded due to nucleotide issues.' % tot_num_non_matching_nts)
    print('Done coordinating genotypes and summary statistics datasets.')




def coordinate_genotypes_ss_w_ld_ref(genotype_file=None,
                                     reference_genotype_file=None,
                                     hdf5_file=None,
                                     genetic_map_dir=None,
                                     check_mafs=False,
                                     min_maf=0.01,
                                     skip_coordination=False, 
                                     debug=False):
    print('Coordinating things w genotype file: %s \nref. genot. file: %s' % (genotype_file, reference_genotype_file))
    
    from plinkio import plinkfile
    plinkf = plinkfile.PlinkFile(genotype_file)

    # Loads only the individuals... 
    plinkf_dict = plinkfiles.get_phenotypes(plinkf)

    # Figure out chromosomes and positions.
    if debug:
        print('Parsing validation bim file')
    loci = plinkf.get_loci()
    plinkf.close()
    gf_chromosomes = [l.chromosome for l in loci]

    chromosomes = sp.unique(gf_chromosomes)
    chromosomes.sort()

    chr_dict = plinkfiles.get_chrom_dict(loci, chromosomes)

    if debug:
        print('Parsing LD reference bim file')
    plinkf_ref = plinkfile.PlinkFile(reference_genotype_file)
    loci_ref = plinkf_ref.get_loci()
    plinkf_ref.close()

    chr_dict_ref = plinkfiles.get_chrom_dict(loci_ref, chromosomes)

    # Open HDF5 file and prepare out data
    assert not 'iids' in hdf5_file, 'Something is wrong with the HDF5 file, no individuals IDs were found.'
    if plinkf_dict['has_phenotype']:
        hdf5_file.create_dataset('y', data=plinkf_dict['phenotypes'])

    hdf5_file.create_dataset('fids', data=sp.array(plinkf_dict['fids'], dtype=util.fids_dtype))
    hdf5_file.create_dataset('iids', data=sp.array(plinkf_dict['iids'], dtype=util.iids_dtype))
    ssf = hdf5_file['sum_stats']
    cord_data_g = hdf5_file.create_group('cord_data')

    maf_adj_risk_scores = sp.zeros(plinkf_dict['num_individs'])
    num_common_snps = 0
    # corr_list = []

    tot_g_ss_nt_concord_count = 0
    tot_rg_ss_nt_concord_count = 0
    tot_g_rg_nt_concord_count = 0
    tot_num_non_matching_nts = 0

    # Now iterate over chromosomes
    for chrom in chromosomes:
        ok_indices = {'g': [], 'rg': [], 'ss': []}

        chr_str = 'chrom_%d' % chrom
        print('Coordinating data for chromosome %s' % chr_str)

        chrom_d = chr_dict[chr_str]
        chrom_d_ref = chr_dict_ref[chr_str]
        try:
            ssg = ssf['chrom_%d' % chrom]
        except Exception as err_str:
            print(err_str)
            print('Did not find chromosome in SS dataset.')
            print('Continuing.')
            continue

        ssg = ssf['chrom_%d' % chrom]
        g_sids = chrom_d['sids']
        rg_sids = chrom_d_ref['sids']
        ss_sids = (ssg['sids'][...]).astype(util.sids_u_dtype)
        if debug:
            print('Found %d SNPs in validation data, %d SNPs in LD reference data, and %d SNPs in summary statistics.' % (len(g_sids), len(rg_sids), len(ss_sids)))
        common_sids = sp.intersect1d(ss_sids, g_sids)
        common_sids = sp.intersect1d(common_sids, rg_sids)
        if debug:
            print('Found %d SNPs on chrom %d that were common across all datasets' % (len(common_sids), chrom))

        ss_snp_map = []
        g_snp_map = []
        rg_snp_map = []

        ss_sid_dict = {}
        for i, sid in enumerate(ss_sids):
            ss_sid_dict[sid] = i

        g_sid_dict = {}
        for i, sid in enumerate(g_sids):
            g_sid_dict[sid] = i

        rg_sid_dict = {}
        for i, sid in enumerate(rg_sids):
            rg_sid_dict[sid] = i

        for sid in common_sids:
            g_snp_map.append(g_sid_dict[sid])

        # order by positions
        g_positions = sp.array(chrom_d['positions'])[g_snp_map]
        order = sp.argsort(g_positions)
        # order = order.tolist()
        g_snp_map = sp.array(g_snp_map)[order]
        g_snp_map = g_snp_map.tolist()
        common_sids = sp.array(common_sids)[order]

        # Get the other two maps
        for sid in common_sids:
            rg_snp_map.append(rg_sid_dict[sid])

        for sid in common_sids:
            ss_snp_map.append(ss_sid_dict[sid])

        g_nts = sp.array(chrom_d['nts'])
        rg_nts = sp.array(chrom_d_ref['nts'])
        rg_nts_ok = sp.array(rg_nts)[rg_snp_map]
        ss_nts = (ssg['nts'][...]).astype(util.nts_u_dtype)
        betas = ssg['betas'][...]
        log_odds = ssg['log_odds'][...]

        if 'freqs' in ssg:
            ss_freqs = ssg['freqs'][...]

        g_ss_nt_concord_count = sp.sum(
            g_nts[g_snp_map] == ss_nts[ss_snp_map]) / 2.0
        rg_ss_nt_concord_count = sp.sum(rg_nts_ok == ss_nts[ss_snp_map]) / 2.0
        g_rg_nt_concord_count = sp.sum(g_nts[g_snp_map] == rg_nts_ok) / 2.0
        if debug:
            print('Nucleotide concordance counts out of %d genotypes: vg-g: %d, vg-ss: %d, g-ss: %d' % (len(g_snp_map), g_rg_nt_concord_count, g_ss_nt_concord_count, rg_ss_nt_concord_count))
        tot_g_ss_nt_concord_count += g_ss_nt_concord_count
        tot_rg_ss_nt_concord_count += rg_ss_nt_concord_count
        tot_g_rg_nt_concord_count += g_rg_nt_concord_count

        num_non_matching_nts = 0
        num_ambig_nts = 0

        # Identifying which SNPs have nucleotides that are ok..
        ok_nts = []
        for g_i, rg_i, ss_i in zip(g_snp_map, rg_snp_map, ss_snp_map):

            # To make sure, is the SNP id the same?
            assert g_sids[g_i] == rg_sids[rg_i] == ss_sids[ss_i], 'Some issues with coordinating the genotypes.'

            g_nt = g_nts[g_i]
            if not skip_coordination:

                rg_nt = rg_nts[rg_i]
                ss_nt = ss_nts[ss_i]

                # Is the nucleotide ambiguous.
                g_nt = [g_nts[g_i][0], g_nts[g_i][1]]
                if tuple(g_nt) in util.ambig_nts:
                    num_ambig_nts += 1
                    tot_num_non_matching_nts += 1
                    continue

                # First check if nucleotide is sane?
                if (not g_nt[0] in util.valid_nts) or (not g_nt[1] in util.valid_nts):
                    num_non_matching_nts += 1
                    tot_num_non_matching_nts += 1
                    continue

                os_g_nt = sp.array(
                    [util.opp_strand_dict[g_nt[0]], util.opp_strand_dict[g_nt[1]]])

                flip_nts = False
                if not ((sp.all(g_nt == ss_nt) or sp.all(os_g_nt == ss_nt)) and (sp.all(g_nt == rg_nt) or sp.all(os_g_nt == rg_nt))):
                    if sp.all(g_nt == rg_nt) or sp.all(os_g_nt == rg_nt):
                        flip_nts = (g_nt[1] == ss_nt[0] and g_nt[0] == ss_nt[1]) or (
                            os_g_nt[1] == ss_nt[0] and os_g_nt[0] == ss_nt[1])
                        # Try flipping the SS nt
                        if flip_nts:
                            betas[ss_i] = -betas[ss_i]
                            log_odds[ss_i] = -log_odds[ss_i]
                            if 'freqs' in ssg:
                                ss_freqs[ss_i] = 1 - ss_freqs[ss_i]
                        else:
                            if debug:
                                print("Nucleotides don't match after all?: g_sid=%s, ss_sid=%s, g_i=%d, ss_i=%d, g_nt=%s, ss_nt=%s" % \
                                      (g_sids[g_i], ss_sids[ss_i], g_i,
                                       ss_i, str(g_nt), str(ss_nt)))
                            num_non_matching_nts += 1
                            tot_num_non_matching_nts += 1
                            continue

                    else:
                        num_non_matching_nts += 1
                        tot_num_non_matching_nts += 1
                        continue
                        # Opposite strand nucleotides

            # everything seems ok.
            ok_indices['g'].append(g_i)
            ok_indices['rg'].append(rg_i)
            ok_indices['ss'].append(ss_i)

            ok_nts.append(g_nt)

        if debug:
            print('%d SNPs had ambiguous nucleotides.' % num_ambig_nts)
            print('%d SNPs were excluded due to nucleotide issues.' % num_non_matching_nts)
            print('%d SNPs were retained on chromosome %d.' % (len(ok_indices['g']), chrom))

        # Resorting by position
        positions = sp.array(chrom_d['positions'])[ok_indices['g']]

        # Now parse SNPs ..
        snp_indices = sp.array(chrom_d['snp_indices'])
        # Pinpoint where the SNPs are in the file.
        snp_indices = snp_indices[ok_indices['g']]
        raw_snps, freqs = plinkfiles.parse_plink_snps(
            genotype_file, snp_indices)

        snp_indices_ref = sp.array(chrom_d_ref['snp_indices'])
        # Pinpoint where the SNPs are in the file.
        snp_indices_ref = snp_indices_ref[ok_indices['rg']]
        raw_ref_snps, freqs_ref = plinkfiles.parse_plink_snps(
            reference_genotype_file, snp_indices_ref)

        snp_stds_ref = sp.sqrt(2 * freqs_ref * (1 - freqs_ref))
        snp_means_ref = freqs_ref * 2

        snp_stds = sp.sqrt(2 * freqs * (1 - freqs))
        snp_means = freqs * 2

        betas = betas[ok_indices['ss']]  
        log_odds = log_odds[ok_indices['ss']]  

        ps = ssg['ps'][...][ok_indices['ss']]
        nts = sp.array(ok_nts)  
        sids = (ssg['sids'][...]).astype(util.sids_u_dtype)
        sids = sids[ok_indices['ss']]


        # Check SNP frequencies..
        if check_mafs and 'freqs' in ssg:
            ss_freqs = ss_freqs[ok_indices['ss']]
            freq_discrepancy_snp = sp.absolute(ss_freqs - (1 - freqs)) > 0.15 #Array of np.bool values
            if sp.any(freq_discrepancy_snp):
                print('Warning: %d SNPs were filtered due to high allele frequency discrepancy between summary statistics and validation sample' % sp.sum(freq_discrepancy_snp))

                # Filter freq_discrepancy_snps
                ok_freq_snps = sp.logical_not(freq_discrepancy_snp)
                raw_snps = raw_snps[ok_freq_snps]
                snp_stds = snp_stds[ok_freq_snps]
                snp_means = snp_means[ok_freq_snps]
                raw_ref_snps = raw_ref_snps[ok_freq_snps]
                snp_stds_ref = snp_stds_ref[ok_freq_snps]
                snp_means_ref = snp_means_ref[ok_freq_snps]
                freqs = freqs[ok_freq_snps]
                freqs_ref = freqs_ref[ok_freq_snps]
                ps = ps[ok_freq_snps]
                positions = positions[ok_freq_snps]
                nts = nts[ok_freq_snps]
                sids = sids[ok_freq_snps]
                betas = betas[ok_freq_snps]
                log_odds = log_odds[ok_freq_snps]

        # Filter minor allele frequency SNPs.
        maf_filter = (freqs > min_maf) * (freqs < (1 - min_maf))
        maf_filter_sum = sp.sum(maf_filter)
        n_snps = len(maf_filter)
        assert maf_filter_sum <= n_snps, "Problems when filtering SNPs with low minor allele frequencies"
        if sp.sum(maf_filter) < n_snps:
            raw_snps = raw_snps[maf_filter]
            snp_stds = snp_stds[maf_filter]
            snp_means = snp_means[maf_filter]
            raw_ref_snps = raw_ref_snps[maf_filter]
            snp_stds_ref = snp_stds_ref[maf_filter]
            snp_means_ref = snp_means_ref[maf_filter]
            freqs = freqs[maf_filter]
            freqs_ref = freqs_ref[maf_filter]
            ps = ps[maf_filter]
            positions = positions[maf_filter]
            nts = nts[maf_filter]
            sids = sids[maf_filter]
            betas = betas[maf_filter]
            log_odds = log_odds[maf_filter]

        maf_adj_prs = sp.dot(log_odds, raw_snps)
        if debug and plinkf_dict['has_phenotype']:
            maf_adj_corr = sp.corrcoef(
                plinkf_dict['phenotypes'], maf_adj_prs)[0, 1]
            print('Log odds, per genotype PRS correlation w phenotypes for chromosome %d was %0.4f' % (chrom, maf_adj_corr))

        genetic_map = []
        if genetic_map_dir is not None:
            with gzip.open(genetic_map_dir + 'chr%d.interpolated_genetic_map.gz' % chrom) as f:
                for line in f:
                    l = line.split()
#                     if l[0] in sid_set:
#                         genetic_map.append(l[0])
        else:
            genetic_map = None

        coord_data_dict = {'chrom': 'chrom_%d' % chrom, 
                           'raw_snps_ref': raw_ref_snps, 
                           'snp_stds_ref': snp_stds_ref, 
                           'snp_means_ref': snp_means_ref, 
                           'freqs_ref': freqs_ref,
                           'ps': ps,
                           'positions': positions,
                           'nts': nts,
                           'sids': sids,
                           'genetic_map': genetic_map,
                           'betas': betas,
                           'log_odds': log_odds,
                           'log_odds_prs': maf_adj_prs,
                           'raw_snps_val':raw_snps,
                           'snp_stds_val':snp_stds,
                           'snp_means_val':snp_means,
                           'freqs_val':freqs}
          
        write_coord_data(cord_data_g, coord_data_dict)
        maf_adj_risk_scores += maf_adj_prs
        num_common_snps += len(betas)

    # Now calculate the prediction r^2
    if debug and plinkf_dict['has_phenotype']:
        maf_adj_corr = sp.corrcoef(
            plinkf_dict['phenotypes'], maf_adj_risk_scores)[0, 1]
        print('Log odds, per PRS correlation for the whole genome was %0.4f (r^2=%0.4f)' % (maf_adj_corr, maf_adj_corr ** 2))
    print('Overall nucleotide concordance counts: g_rg: %d, g_ss: %d, rg_ss: %d' % (tot_g_rg_nt_concord_count, tot_g_ss_nt_concord_count, tot_rg_ss_nt_concord_count))
    print('There were %d SNPs in common' % num_common_snps)
    print('In all, %d SNPs were excluded due to nucleotide issues.' % tot_num_non_matching_nts)
    print('Done!')




def main(p_dict):

    summary_dict = {}
    
    bimfile = None
    if p_dict['N'] is None:
        print('Please specify an integer value for the sample size used to calculate the GWAS summary statistics.')
    print('Preparing to parse summary statistics')
    if p_dict['vbim'] is not None:
        bimfile = p_dict['vbim']
    elif p_dict['vgf'] is not None:
        bimfile = p_dict['vgf'] + '.bim'
    elif p_dict['gf'] is not None:
        bimfile = p_dict['gf'] + '.bim'
    else:
        print('Set of validation SNPs is missing!  Please specify either a validation PLINK genotype file, ' \
              'or a PLINK BIM file with the SNPs of interest.')
    if os.path.isfile(p_dict['out']):
        print('Output file (%s) already exists!  Delete, rename it, or use a different output file.'\
              % (p_dict['out']))
        raise Exception('Output file already exists!')

    h5f = h5py.File(p_dict['out'], 'w')
    
    sum_stats_parsers.parse_sum_stats(h5f, p_dict, bimfile)
    check_mafs = p_dict['maf']>0
    if not p_dict['vgf'] == None:
        coordinate_genotypes_ss_w_ld_ref(genotype_file=p_dict['vgf'], reference_genotype_file=p_dict['gf'],
                                         check_mafs=check_mafs,
                                         hdf5_file=h5f, min_maf=p_dict['maf'], skip_coordination=p_dict['skip_coordination'], 
                                         debug=p_dict['debug'])
    else:
        coordinate_genot_ss(genotype_file=p_dict['gf'], check_mafs=check_mafs,
                            hdf5_file=h5f, min_maf=p_dict['maf'], skip_coordination=p_dict['skip_coordination'], 
                            debug=p_dict['debug'])

    

    h5f.close()
