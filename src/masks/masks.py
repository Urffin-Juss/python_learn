from logg_func import patch_module_with_logging
import sys





patch_module_with_logging(sys.modules[__name__], 'log_masks.log')