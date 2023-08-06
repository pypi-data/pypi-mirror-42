from janis_bioinformatics.data_types import Bam, BamBai, Fastq, Sam, FastaWithDict
from janis_bioinformatics.tools import BioinformaticsWorkflow
from janis_bioinformatics.tools.bwa import BwaMemLatest
from janis_bioinformatics.tools.gatk4 import Gatk4SortSamLatest
from janis_bioinformatics.tools.samtools import SamToolsViewLatest
from janis import Step, String, Input, Directory, Output
from janis.utils.metadata import WorkflowMetadata


class AlignSortedBam(BioinformaticsWorkflow):

    def __init__(self):
        super(AlignSortedBam, self).__init__("alignsortedbam", friendly_name="Align sorted BAM")

        if not self._metadata:
            self._metadata = WorkflowMetadata()

        self._metadata.documentation = "Align sorted bam with this subworkflow consisting of BWA Mem + SamTools + Gatk4SortSam"
        self._metadata.creator = "Michael Franklin"
        self._metadata.dateCreated = "2018-12-24"
        self._metadata.version = "1.0.0"

        s1_bwa = Step("s1_bwa", BwaMemLatest())
        s2_samtools = Step("s2_samtools", SamToolsViewLatest())
        s3_sortsam = Step("s3_sortsam", Gatk4SortSamLatest())

        s1_inp_header = Input("read_group_header_line", String())
        s1_inp_reference = Input("reference", FastaWithDict())
        s1_inp_fastq = Input("fastq", Fastq())

        s3_inp_tmpdir = Input("tmpdir", Directory())

        out_bwa = Output("out_bwa", Sam())
        out_samtools = Output("out_samtools", Bam())
        out_sortsam = Output("out_sortsam", BamBai())
        out = Output("out", BamBai())

        # Fully connect step 1
        self.add_edges([
            (s1_inp_header, s1_bwa.readGroupHeaderLine),
            (s1_inp_fastq, s1_bwa.reads),
            (s1_inp_reference, s1_bwa.reference)
        ])
        self.add_default_value(s1_bwa.threads, 36)

        # fully connect step 2
        self.add_edge(s1_bwa.out, s2_samtools.sam)

        # fully connect step 3
        self.add_edges([
            (s2_samtools.out, s3_sortsam.bam),
            (s3_inp_tmpdir, s3_sortsam.tmpDir),
        ])
        self.add_default_value(s3_sortsam.sortOrder, "coordinate")
        self.add_default_value(s3_sortsam.createIndex, True)
        self.add_default_value(s3_sortsam.validationStringency, "SILENT")
        self.add_default_value(s3_sortsam.maxRecordsInRam, 5000000)

        # connect to output
        self.add_edge(s1_bwa.out, out_bwa)
        self.add_edge(s2_samtools.out, out_samtools)
        self.add_edge(s3_sortsam.out, out_sortsam)
        self.add_edge(s3_sortsam.out, out)


if __name__ == "__main__":
    w = AlignSortedBam()
    w.dump_translation("wdl")
    # print(AlignSortedBam().help())
