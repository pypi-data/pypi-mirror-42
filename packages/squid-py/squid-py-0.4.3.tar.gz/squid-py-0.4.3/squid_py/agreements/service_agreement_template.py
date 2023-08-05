import json

from squid_py.agreements.service_agreement_condition import ServiceAgreementCondition
from squid_py.agreements.service_agreement_contract import ServiceAgreementContract


class ServiceAgreementTemplate(object):
    DOCUMENT_TYPE = 'OceanProtocolServiceAgreementTemplate'
    TEMPLATE_ID_KEY = 'templateId'

    def __init__(self, template_json=None):
        self.template_id = ''
        self.name = ''
        self.creator = ''
        self.conditions = []
        self.service_agreement_contract = None
        if template_json:
            self.parse_template_json(template_json)

    @classmethod
    def from_json_file(cls, path):
        with open(path) as jsf:
            template_json = json.load(jsf)
            return cls(template_json=template_json)

    @staticmethod
    def compress_dep_timeout_values(dependency_list, timeout_flags_list):
        compressed_dep_value = 0
        num_bits = 2  # 1st for dependency, 2nd for timeout flag
        for i, d in enumerate(dependency_list):
            t = timeout_flags_list[i]
            offset = i * num_bits
            compressed_dep_value |= d * 2 ** (offset + 0)  # the dependency bit
            compressed_dep_value |= t * 2 ** (offset + 1)  # the timeout bit

        return compressed_dep_value

    @property
    def conditions_dependencies(self):
        """
        Build a list of dependencies to represent how each condition in this service agreement
        template depend on other conditions.
        Each value in the dependencies list is an integer that compresses the dependency and
        timeout flag corresponding to each
        condition in the list of all conditions.
        Each condition is assigned 2 bits:
        - first/right bit denotes dependency: 1 is a dependency, 0 not a dependency
        - second/left bit denotes timeout flag: 1 means dependency relies on timeout of parent
        condition, 0 no timeout necessary

        Note that timeout flag must not be set to 1 if the dependency is 0.

        This compressed format is necessary to avoid limitations of the `solidity` language which
        is used to implement the EVM smart
        contracts.
        :return: list of integers
        """
        compressed_dependencies = []
        for i, cond in enumerate(self.conditions):
            assert len(cond.dependencies) == len(
                cond.timeout_flags), 'Invalid dependencies and timeout_flags, they are required ' \
                                     'to have the same length.'
            dep = []
            tout_flags = []
            for j in range(len(self.conditions)):
                other_cond_name = self.conditions[j].name
                if i != j and other_cond_name in cond.dependencies:
                    dep.append(1)
                    tout_flags.append(cond.timeout_flags[cond.dependencies.index(other_cond_name)])
                else:
                    dep.append(0)
                    tout_flags.append(0)

            assert len(dep) == len(tout_flags), ''
            assert len(dep) == len(self.conditions)
            compressed_dependencies.append(
                ServiceAgreementTemplate.compress_dep_timeout_values(dep, tout_flags)
            )

        return compressed_dependencies

    def parse_template_json(self, template_json):
        assert template_json['type'] == self.DOCUMENT_TYPE, ''
        self.template_id = template_json['id']
        self.name = template_json['name']
        self.creator = template_json['creator']
        self.conditions = [ServiceAgreementCondition(cond_json) for cond_json in
                           template_json['conditions']]
        self.service_agreement_contract = ServiceAgreementContract(
            template_json['serviceAgreementContract'])

    def as_dictionary(self):
        return {
            'type': self.DOCUMENT_TYPE,
            'id': self.template_id,
            'name': self.name,
            'creator': self.creator,
            'serviceAgreementContract': self.service_agreement_contract.as_dictionary(),
            'conditions': [cond.as_dictionary() for cond in self.conditions],
        }

    @staticmethod
    def example_dict():
        return {
            "type": "OceanProtocolServiceAgreementTemplate",
            "id": "0x044852b2a670ade5407e78fb2863c51de9fcb96542a07186fe3aeda6bb8a116d",
            "name": "dataAssetAccessServiceAgreement",
            "creator": "",
            "serviceAgreementContract": {
                "contractName": "ServiceExecutionAgreement",
                "fulfillmentOperator": 1,
                "events": [
                    {
                        "name": "AgreementInitialized",
                        "actorType": "consumer",
                        "handler": {
                            "moduleName": "payment",
                            "functionName": "lockPayment",
                            "version": "0.1"
                        }
                    }
                ]
            },
            "conditions": [
                {
                    "name": "lockPayment",
                    "timeout": 0,
                    "conditionKey": "",
                    "contractName": "PaymentConditions",
                    "functionName": "lockPayment",
                    "index": 0,
                    "parameters": [
                        {
                            "name": "assetId",
                            "type": "bytes32",
                            "value": ""
                        }, {
                            "name": "price",
                            "type": "uint256",
                            "value": ""
                        }
                    ],
                    "events": [
                        {
                            "name": "PaymentLocked",
                            "actorType": "publisher",
                            "handler": {
                                "moduleName": "accessControl",
                                "functionName": "grantAccess",
                                "version": "0.1"
                            }
                        }
                    ],
                    "dependencies": [],
                    "isTerminalCondition": 0
                }, {
                    "name": "grantAccess",
                    "timeout": 0,
                    "conditionKey": "",
                    "contractName": "AccessConditions",
                    "functionName": "grantAccess",
                    "index": 1,
                    "parameters": [
                        {
                            "name": "documentKeyId",
                            "type": "bytes32",
                            "value": ""
                        }
                    ],
                    "events": [
                        {
                            "name": "AccessGranted",
                            "actorType": "publisher",
                            "handler": {
                                "moduleName": "payment",
                                "functionName": "releasePayment",
                                "version": "0.1"
                            }
                        },
                        {
                            "name": "AccessGranted",
                            "actorType": "consumer",
                            "handler": {
                                "moduleName": "accessControl",
                                "functionName": "consumeAsset",
                                "version": "0.1"
                            }
                        },
                        {
                            "name": "AccessTimeout",
                            "actorType": "consumer",
                            "handler": {
                                "moduleName": "payment",
                                "functionName": "refundPayment",
                                "version": "0.1"
                            }
                        }
                    ],
                    "dependencies": [
                        {
                            "name": "lockPayment",
                            "timeout": 0
                        }
                    ],
                    "isTerminalCondition": 0
                }, {
                    "name": "releasePayment",
                    "timeout": 0,
                    "conditionKey": "",
                    "contractName": "PaymentConditions",
                    "functionName": "releasePayment",
                    "index": 2,
                    "parameters": [
                        {
                            "name": "assetId",
                            "type": "bytes32",
                            "value": ""
                        }, {
                            "name": "price",
                            "type": "uint256",
                            "value": ""
                        }
                    ],
                    "events": [
                        {
                            "name": "PaymentReleased",
                            "actorType": "consumer",
                            "handler": {
                                "moduleName": "serviceAgreement",
                                "functionName": "fulfillAgreement",
                                "version": "0.1"
                            }
                        }
                    ],
                    "dependencies": [
                        {
                            "name": "grantAccess",
                            "timeout": 0
                        }
                    ],
                    "isTerminalCondition": 1
                }, {
                    "name": "refundPayment",
                    "timeout": 1,
                    "conditionKey": "",
                    "contractName": "PaymentConditions",
                    "functionName": "refundPayment",
                    "index": 3,
                    "parameters": [
                        {
                            "name": "assetId",
                            "type": "bytes32",
                            "value": ""
                        }, {
                            "name": "price",
                            "type": "uint256",
                            "value": ""
                        }
                    ],
                    "events": [
                        {
                            "name": "PaymentRefund",
                            "actorType": "consumer",
                            "handler": {
                                "moduleName": "serviceAgreement",
                                "functionName": "terminateAgreement",
                                "version": "0.1"
                            }
                        }
                    ],
                    "dependencies": [
                        {
                            "name": "lockPayment",
                            "timeout": 0
                        },
                        {
                            "name": "grantAccess",
                            "timeout": 1
                        }
                    ],
                    "isTerminalCondition": 1
                }
            ]
        }
