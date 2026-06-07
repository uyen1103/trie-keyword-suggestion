import customtkinter as ctk

# =========================
# Cấu hình giao diện
# =========================
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


class MainWindow(ctk.CTk):

    def __init__(
        self,
        search_callback,
        select_callback,
        stats_callback=None,
        history_callback=None
    ):
        super().__init__()

        # Callback
        self.search_callback = search_callback
        self.select_callback = select_callback
        self.stats_callback = stats_callback
        self.history_callback = history_callback

        # Cửa sổ chính
        self.title("Keyword Suggestion System")
        self.geometry("800x550")
        self.resizable(False, False)

        self._build_ui()

    def _build_ui(self):

        # =========================
        # Frame chính
        # =========================
        self.main_frame = ctk.CTkFrame(
            self,
            corner_radius=15
        )

        self.main_frame.pack(
            padx=30,
            pady=30,
            fill="both",
            expand=True
        )

        # =========================
        # Tiêu đề
        # =========================
        self.title_label = ctk.CTkLabel(
            self.main_frame,
            text="🔍 HỆ THỐNG GỢI Ý TỪ KHÓA",
            font=("Arial", 28, "bold")
        )

        self.title_label.pack(
            pady=(25, 10)
        )

        self.subtitle = ctk.CTkLabel(
            self.main_frame,
            text="Nhập tiền tố để nhận các từ gợi ý từ Trie",
            font=("Arial", 14)
        )

        self.subtitle.pack(
            pady=(0, 20)
        )

        # =========================
        # Thanh tìm kiếm
        # =========================
        self.search_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color="transparent"
        )

        self.search_frame.pack(
            pady=10
        )

        self.search_entry = ctk.CTkEntry(
            self.search_frame,
            width=450,
            height=40,
            placeholder_text="Nhập từ khóa..."
        )

        self.search_entry.pack(
            side="left",
            padx=10
        )

        # Tự động tìm khi gõ
        self.search_entry.bind(
            "<KeyRelease>",
            self._on_search
        )

        self.search_button = ctk.CTkButton(
            self.search_frame,
            text="Tìm kiếm",
            width=120,
            height=40,
            state="disabled"
        )

        self.search_button.pack(
            side="left"
        )

        # =========================
        # Tiêu đề kết quả
        # =========================
        self.result_label = ctk.CTkLabel(
            self.main_frame,
            text="Danh sách gợi ý",
            font=("Arial", 18, "bold")
        )

        self.result_label.pack(
            pady=(25, 10)
        )

        # =========================
        # ScrollableFrame
        # =========================
        self.suggestion_frame = ctk.CTkScrollableFrame(
            self.main_frame,
            width=600,
            height=220,
            corner_radius=10
        )

        self.suggestion_frame.pack(
            pady=10
        )

        # Hiển thị dữ liệu mẫu
        self.show_suggestions([
            "apple",
            "application",
            "apply",
            "appstore"
        ])

        # =========================
        # Footer
        # =========================
        self.footer = ctk.CTkLabel(
            self.main_frame,
            text="Trie Keyword Suggestion System © 2025",
            font=("Arial", 12)
        )

        self.footer.pack(
            side="bottom",
            pady=15
        )

    # =========================
    # Khi người dùng gõ
    # =========================
    def _on_search(self, event):

        prefix = self.search_entry.get()

        suggestions = self.search_callback(
            prefix
        )

        self.show_suggestions(
            suggestions
        )

    # =========================
    # Hiển thị gợi ý
    # =========================
    def show_suggestions(self, words):

        # Xóa các button cũ
        for widget in self.suggestion_frame.winfo_children():
            widget.destroy()

        # Tạo button mới
        for word in words:

            btn = ctk.CTkButton(
                self.suggestion_frame,
                text=word,
                height=35,
                anchor="w",
                command=lambda w=word:
                    self.select_callback(w)
            )

            btn.pack(
                fill="x",
                pady=2,
                padx=5
            )


# ====================================
# Test Mock
# ====================================

if __name__ == "__main__":

    demo_words = [
        "apple",
        "application",
        "apply",
        "appstore",
        "banana",
        "bank",
        "basket",
        "code",
        "coding",
        "computer"
    ]

    def mock_search(prefix):

        if prefix == "":
            return demo_words

        return [
            word
            for word in demo_words
            if word.startswith(
                prefix.lower()
            )
        ]

    def mock_select(word):

        print(
            f"Đã chọn: {word}"
        )

    app = MainWindow(
        search_callback=mock_search,
        select_callback=mock_select
    )

    app.mainloop()