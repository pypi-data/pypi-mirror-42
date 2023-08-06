from cerebralcortex.data_importer.data_parsers import mcerebrum_data_parser
from cerebralcortex.data_importer.metadata_parsers import mcerebrum_metadata_parser
from cerebralcortex.data_importer import import_dir

import_dir(
    cc_config="/home/ali/IdeaProjects/CerebralCortex-2.0/conf/",
    input_data_dir="/home/ali/IdeaProjects/MD2K_DATA/data/test/",
    batch_size=20,
    compression='gzip',
    header=None,
    data_file_extension=[".gz"],
    # allowed_filename_pattern="REGEX PATTERN",
    data_parser=mcerebrum_data_parser,
    metadata_parser=mcerebrum_metadata_parser,
    gen_report=True
)