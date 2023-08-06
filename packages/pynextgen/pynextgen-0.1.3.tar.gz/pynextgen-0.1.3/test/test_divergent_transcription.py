import os
import pytest
import subprocess
from easydev import md5
import shutil
import pynextgen.divtrans as dt
import pynextgen.basics_bam as bb


REF_DIR = "test/divtrans/"
FOS_BAM = "vehicule_fos_area.bam"


@pytest.fixture(scope="module")
def final_cleanup(request):
    def teardown():

        files_to_remove = ["common.log", "bedpe.log"]

        for f in files_to_remove:
            os.remove(f)

    request.addfinalizer(teardown)


@pytest.fixture(scope="function")
def setup_fos(tmpdir):
    shutil.copy(os.path.join("test/divtrans", FOS_BAM), tmpdir)


def test_divergent_transcription_cli(setup_fos, tmpdir):
    """ Test the divergent_transcription.py script
    """

    cmd = f"python pynextgen/scripts/divergent_transcription.py {tmpdir.join(FOS_BAM)}"

    subprocess.check_output(cmd, shell=True)


def test_fos_from_bam(final_cleanup, setup_fos, tmpdir):
    """ Test detection of divergent transcription in the mini FOS dataset
    """

    # From bam fragments
    divtrans = dt.DivTransFromBam(str(tmpdir.join(FOS_BAM)), distance=500, reuse=False)
    divtrans.run()

    assert md5(divtrans.bed.path) == md5(REF_DIR + "vehicule_fos_area_divtrans_REF.bed")

    # Testing count filtering
    divtrans.filter_by_counts(
        "test/divtrans/hg19.genome", flank=500, count_thres=1, count_ratio_thres=1
    )
    divtrans.clean()

    # assert md5(divtrans.filtered_bed.path) == md5(
    #    REF_DIR + "vehicule_fos_area_divtrans_count_filtered.bed"
    # )

    # From fragments computed with bedtools (old version)


def test_fos_from_bed(final_cleanup, setup_fos, tmpdir):

    divtrans_from_bed = dt.DivTransFromBed(str(tmpdir.join(FOS_BAM)))
    divtrans_from_bed.run()

    print(divtrans_from_bed.divtrans_bed.path)

    assert md5(divtrans_from_bed.divtrans_bed.path) == md5(
        REF_DIR + "vehicule_fos_area_divtrans_from_bed.bed"
    )


def test_case_divtrans(tmpdir):
    """Test different cases of reads positionning which should lead, or
    not to the detection of a divergent transcription event """

    bam = bb.generate_bam(
        tmpdir.join("basic.bam"),
        "test/divtrans/bam_header.sam",
        "test/divtrans/reads_for_bam.tsv",
    ).path

    divtrans = dt.DivTransFromBam(
        bam, distance=200, max_template_length=400, reuse=False, no_overlap=False
    )
    divtrans.run()

    assert md5(divtrans.bed.path) == md5(REF_DIR + "basic.bed")
