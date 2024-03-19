The fasta files as output from PEMA processing for batch1 (see folder above for details on the batch1 processing). 
Within these files, each row contains an identifier+the DNA sequence. This identifier is also used in the [taxonomic assignment files](https://github.com/arms-mbon/data_workspace/tree/main/analysis_data/from_pema/processing_batch1/taxonomic_assignments), so you can match the information in these files in this way. Note that the date in the filename refers to the date of sequencing, rather than the date of the sampling event.

For COI and ITS:
* The files called __all_samples_xxx__ contain all the sequences found in all samples. The sequence identifiers are of the format ID;size=readAbundance. These are the input files for the clustering algorithm.
* The files called __all_sequences_grouped_xxx__ contain the sequences remaining after chimera removal and clustering. The sequence identifiers are of the format ID_readAbundance. Because there was an error within PEMA at the time of usage regarding the sequence identifier format, the ITS sequence identifiers in these files are of the format OtuXY.

For 18S:
* The files called __Aligned_assignments_xxx__ contain two lines per ASV/OTU, the first is the identifier followed by the taxonomy, the second is the sequence
* The files called final_all_samples_xxx: contain individual sample files (.fasta) but only with the sequences that remained after the quality control and the pre-processing steps; thess are used to form a single .fasta (“final_all_samples.fasta”). This is the file PEMA uses from this point onwards for the clustering and taxonomy assignment steps. 

The files are too large to store here in GitHub, so they have been placed in the Marine Data Archive for access. 
The download URL for these files are the following:

| filename | download URL | 
| --- | --- |
| all_samples_April2021_COI.fasta| [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5aea4e8594692446647](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5aea4e8594692446647)  |
|all_samples_January2020_COI.fasta | [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5aea4e8731452238120](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5aea4e8731452238120)  |
|all_samples_January2022_COI.fasta| [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5aea4e87d8415011086](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5aea4e87d8415011086) |
|all_samples_July2019_COI.fasta| [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5aea4e8979356562781](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5aea4e8979356562781) |
|all_samples_May2021_COI.fasta| [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5aea4e8678040464373](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5aea4e8678040464373) |
|all_samples_September2020_COI.fasta| [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5aec1c6fab524389208](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5aec1c6fab524389208) |
|all_samples_August2023_COI.fasta | [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_65ddecfdd40a6306869705](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_65ddecfdd40a6306869705)|
|all_samples_ARMS_Gdynia_GDY1_20180813_20191029_SF38_DMSO_COI.fasta | [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_65ddecfdd4616135376976](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_65ddecfdd4616135376976)|
|all_sequences_grouped_April2021_COI.fa| [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5aec1c61d2304932779](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5aec1c61d2304932779) |
|all_sequences_grouped_January2020_COI.fa| [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5aec1d37cd080876413](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5aec1d37cd080876413) |
|all_sequences_grouped_January2022_COI.fa|[https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5aec1c9cc8783258670](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5aec1c9cc8783258670)  |
|all_sequences_grouped_July2019_COI.fa|[https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5aec1c8507131186606](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5aec1c8507131186606)  |
|all_sequences_grouped_May2021_COI.fa| [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5aec1d22f7293220847](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5aec1d22f7293220847) |
|all_sequences_grouped_September2020_COI.fa| [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5aec1ce619790794228](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5aec1ce619790794228) |
|all_sequences_grouped_August2023_COI.fa | [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_65ddecfdd4817905877667](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_65ddecfdd4817905877667)|
|all_sequences_grouped_ARMS_Gdynia_GDY1_20180813_20191029_SF38_DMSO_COI.fa | [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_65ddecfdd3dbd317188875](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_65ddecfdd3dbd317188875)|
|Aligned_assignments_April2021_18S.fasta| [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c30492304947055810](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c30492304947055810) |
|Aligned_assignments_January2020_18S.fasta| [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c304a6079692934739](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c304a6079692934739) |
|Aligned_assignments_January2022_18S.fasta| [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c304974c2824435732](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c304974c2824435732) |
|Aligned_assignments_July2019_18S.fasta| [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c3049223a375779320](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c3049223a375779320) |
|Aligned_assignments_May2021_18S.fasta| [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c304a04ec570416353](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c304a04ec570416353) |
|Aligned_assignments_September2020_18S.fasta| [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c30495306133353334](	https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c30495306133353334) |
|Aligned_assignments_August2023_18S.fasta | [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_65ddecfdd3c8b943104041](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_65ddecfdd3c8b943104041)|
|Aligned_assignments_ARMS_Gdynia_GDY1_20180813_20191029_SF38_DMSO_18S.fasta | [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_65ddecfdd4483691581806](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_65ddecfdd4483691581806)|
|all_sequences_grouped_April2021_18S.fa| [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c30492143175479550](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c30492143175479550) |
|all_sequences_grouped_January2020_18S.fa| [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c304922d2186250508](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c304922d2186250508) |
|all_sequences_grouped_January2022_18S.fa| [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c304921f8455298820](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c304921f8455298820) |
|all_sequences_grouped_July2019_18S.fa| [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c304a777b329215005](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c304a777b329215005) |
|all_sequences_grouped_May2021_18S.fa| [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c304924df142213445](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c304924df142213445) |
|all_sequences_grouped_September2020_18S.fa| [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c304970ae592926655](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c304970ae592926655) |
|all_sequences_grouped_August2023_18S.fa | [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_65ddecfdd442c260357887](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_65ddecfdd442c260357887)|
|all_sequences_grouped_ARMS_Gdynia_GDY1_20180813_20191029_SF38_DMSO_18S.fa | [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_65ddecfdd4716735408577](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_65ddecfdd4716735408577)|
|final_all_samples_April2021_18S.fasta| [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c37c8b956716621278](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c37c8b956716621278) |
|final_all_samples_January2020_18S.fasta| [	https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c37c813a3970262799](	https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c37c813a3970262799) |
|final_all_samples_January2022_18S.fasta| [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c37c83730731111561](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c37c83730731111561) |
|final_all_samples_July2019_18S.fasta| [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c37c7eea9982641559](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c37c7eea9982641559) |
|final_all_samples_May2021_18S.fasta| [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c37c80227525079610](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c37c80227525079610) |
|final_all_samples_September2020_18S.fasta| [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c37c868fd846188990](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c37c868fd846188990) |
|final_all_samples_August2023_18S.fasta | [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_65ddecfdd3cff387444744](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_65ddecfdd3cff387444744)|
|final_all_samples_ARMS_Gdynia_GDY1_20180813_20191029_SF38_DMSO_18S.fasta | [https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_65ddecfdd4467209313990](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_65ddecfdd4467209313990)|
|Aligned_assignments_April2021_ITS.fasta|[https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c72a7dc04901354082](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c72a7dc04901354082)|
|Aligned_assignments_July2019_ITS.fasta|[https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c72a6455c030029062](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c72a6455c030029062)|
|all_samples_April2021_ITS.fasta|[https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c72a7dee9117163394](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c72a7dee9117163394)|
|all_samples_July2019_ITS.fasta|[https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c72a7e07e102126946](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c72a7e07e102126946)|
|all_sequences_grouped_April2021_ITS.fa|[https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c72a64286428025677](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c72a64286428025677)|
|all_sequences_grouped_July2019_ITS.fa|[https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c72a7dc04477203942](https://mda.vliz.be/directlink.php?fid=VLIZ_00000615_64e5c72a7dc04477203942)|
