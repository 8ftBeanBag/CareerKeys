import threading

class ScraperThreads:
    threads = []
    
    def add_thread(self, function, args):
        # Only run up to 100 threads
        if len(self.threads) > 10:
            self.threads[len(self.threads) - 1].join()
            print("last thread joined, adding new one")
        self.threads.append(threading.Thread(target=function, args=args))