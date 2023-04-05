from tqdm import tqdm
from queue import Queue

# tqdm_list = [1]
order_q = Queue()  # TODO put a limit
pb_order = tqdm([], colour='green')  # iter(order_q.queue)
# pb_order.total=1
pb = pb_order
