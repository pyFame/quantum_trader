from queue import Queue

from utils.progress_bar import ProgresBar, MAGENTA

# tqdm_list = [1]
order_q = Queue(10)

# # progress bar
# pb = tqdm([], colour='green')  # iter(order_q.queue)
# # pb_order.total=1


pb = ProgresBar(color=MAGENTA)
