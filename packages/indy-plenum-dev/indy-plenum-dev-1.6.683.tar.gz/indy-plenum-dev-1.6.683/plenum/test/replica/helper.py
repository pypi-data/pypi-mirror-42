import time

from plenum.common.constants import CURRENT_PROTOCOL_VERSION, DOMAIN_LEDGER_ID
from plenum.test.helper import sdk_random_request_objects


def emulate_catchup(replica, ppSeqNo=100):
    replica.on_catch_up_finished(last_caught_up_3PC=(replica.viewNo, ppSeqNo),
                                 master_last_ordered_3PC=replica.last_ordered_3pc)


def emulate_select_primaries(replica):
    replica.primaryName = 'SomeAnotherNode'
    replica._setup_for_non_master_after_view_change(replica.viewNo)


def create_preprepare(replica, sdk_wallet_steward, req_count):
    _, did = sdk_wallet_steward
    reqs = sdk_random_request_objects(req_count, identifier=did,
                                      protocol_version=CURRENT_PROTOCOL_VERSION)
    for req in reqs:
        replica.requestQueues[DOMAIN_LEDGER_ID].add(req.key)
        replica.requests.add(req)
        replica.requests.set_finalised(req)
    replica.last_accepted_pre_prepare_time = int(time.time())
    pp = replica.create_3pc_batch(DOMAIN_LEDGER_ID)
    return reqs, pp
