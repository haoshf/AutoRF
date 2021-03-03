import json


class Contract(object):
    def __init__(self):
        self.contract = {
            '档案编号': 'fileNumber',
            '审批单号': 'approvalNumber',
            '发起人': 'promoter',
            '合同名称': 'contractName',
            '合同签约主体': 'contractSignSubject',
            '供应商名称': 'supplierName',
            '客户名称': 'customerName',
            '文件类型': 'fileType',
            '合同类型': 'contractType',
            '合同金额': 'contractAmount',
            '合同起始日期': 'contractStartDate',
            '合同终止日期': 'contractEndDate',
            '合同到期是否延续': 'renewFlag',
            '项目取得方式': 'projectRequiredType',
            '客户联系方式': 'customerContact',
            '合同附件': 'contractAttachment',
            '备注': 'remark',
            '合同状态': 'contractState'
        }

    def add_contract(self, **kwargs):

        contract_mes = {
            "approvalNumber": "",
            "contractAmount": "",
            "contractAttachment": "0",
            "contractEndDate": "",
            "contractId": "",
            "contractName": "",
            "contractSignSubject": "",
            "contractStartDate": "",
            "contractState": "",
            "contractType": "",
            "customerContact": "",
            "customerName": "",
            "fileNumber": "",
            "fileType": "",
            "projectRequiredType": "",
            "promoter": "",
            "remark": "",
            "renewFlag": "",
            "supplierName": ""
        }
        for key, value in kwargs.items():
            contract_mes[self.contract[key]] = value

        return json.dumps(contract_mes)

    def up_contract(self, contract_detail, **kwargs):

        contract_mes = contract_detail['data']
        for key, value in kwargs.items():
            contract_mes[self.contract[key]] = value

        return json.dumps(contract_mes)
