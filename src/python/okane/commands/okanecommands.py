import okane.commands.updateaccounts as command_updateaccounts
import okane.commands.saveaccounts as command_saveaccounts
import okane.commands.listaccounts as command_listaccounts
import okane.commands.deleteaccount as command_deleteaccount
import okane.commands.listregisters as command_listregisters
import okane.commands.updatecategory as command_updatecategory
import okane.commands.listcategories as command_listcategories
import okane.commands.savecategory as command_savecategory
import okane.commands.deletecategory as command_deletecategory
import okane.commands.saveregister as command_saveregister
import okane.commands.deleteregister as command_deleteregister
import okane.commands.updateregister as command_updateregister
import okane.commands.showbalance as command_showbalance
import okane.commands.showbalanceperaccount as command_showbalanceperaccount
import okane.commands.showbalancepercategory as command_showbalancepercategory
import okane.commands.showbalancethroughtime as command_showbalancethroughtime
import okane.commands.transferoperation as command_transferoperation
import okane.commands.listrecurrentregisters as command_listrecurrentregisters
import okane.commands.deleterecurrentregisters as command_deleterecurrentregister
import okane.commands.importcsv as command_importcsv
import okane.commands.exportcsv  as command_exportcsv
import okane.commands.exportjson  as command_exportjson
import okane.commands.xlsloading as command_xlsloading
import okane.commands.help as command_help


def get_commands():
    return [
            command_saveregister,
            command_listregisters,
            command_updateregister,
            command_listaccounts,
            command_saveaccounts,
            command_updateaccounts,
            command_deleteaccount,
            command_updatecategory,
            command_listcategories,
            command_savecategory,
            command_deletecategory,
            command_deleteregister,
            command_showbalance,
            command_showbalanceperaccount,
            command_showbalancepercategory,
            command_showbalancethroughtime,
            command_transferoperation,
            command_listrecurrentregisters,
            command_deleterecurrentregister,
            command_importcsv,
            command_exportcsv,
            command_exportjson,
            command_xlsloading,
            command_help
        ]
