from queue import Queue
from tqdm import tqdm

buys = Queue()  # FIXME add a number
sells = Queue()

# tqdm_list = [1]
signals_q = Queue()  # TODO put a limit

# progress bar
pb_order = tqdm([], colour='green')  # iter(order_q.queue)
# pb_order.total=1
pb = pb_order
