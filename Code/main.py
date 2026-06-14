# main.py
# Application entry point for trie keyword suggestion

from .app_controller import AppController
from .gui import MainWindow
 
 
def main():
    controller = AppController(top_k=5)
 
    app = MainWindow(
        search_callback=controller.search,
        select_callback=controller.on_select,
        stats_callback=controller.stats,
        history_callback=controller.get_history
    )
 
    # Đóng DB khi cửa sổ bị tắt
    def on_close():
        controller.close()
        app.destroy()

    app.protocol("WM_DELETE_WINDOW", on_close)
    
    app.mainloop()
 
 
if __name__ == "__main__":
    main()
 
