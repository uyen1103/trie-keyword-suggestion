# gui.py

import customtkinter as ctk

# Cấu hình giao diện
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Cửa sổ chính
app = ctk.CTk()
app.title("Keyword Suggestion System")
app.geometry("800x550")
app.resizable(False, False)

# Frame chính
main_frame = ctk.CTkFrame(
    app,
    corner_radius=15
)
main_frame.pack(
    padx=30,
    pady=30,
    fill="both",
    expand=True
)

# Tiêu đề
title = ctk.CTkLabel(
    main_frame,
    text="🔍 HỆ THỐNG GỢI Ý TỪ KHÓA",
    font=("Arial", 28, "bold")
)
title.pack(pady=(25, 10))

subtitle = ctk.CTkLabel(
    main_frame,
    text="Nhập tiền tố để nhận các từ gợi ý từ Trie",
    font=("Arial", 14)
)
subtitle.pack(pady=(0, 20))

# Thanh tìm kiếm
search_frame = ctk.CTkFrame(
    main_frame,
    fg_color="transparent"
)
search_frame.pack(pady=10)

search_entry = ctk.CTkEntry(
    search_frame,
    width=450,
    height=40,
    placeholder_text="Nhập từ khóa..."
)
search_entry.pack(side="left", padx=10)

search_button = ctk.CTkButton(
    search_frame,
    text="Tìm kiếm",
    width=120,
    height=40
)
search_button.pack(side="left")

# Tiêu đề vùng kết quả
result_label = ctk.CTkLabel(
    main_frame,
    text="Danh sách gợi ý",
    font=("Arial", 18, "bold")
)
result_label.pack(pady=(25, 10))

# Hộp gợi ý
suggestion_box = ctk.CTkTextbox(
    main_frame,
    width=600,
    height=220,
    corner_radius=10,
    font=("Consolas", 15)
)
suggestion_box.pack(pady=10)

# Dữ liệu mẫu
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

for word in demo_words:
    suggestion_box.insert("end", f"• {word}\n")

# Footer
footer = ctk.CTkLabel(
    main_frame,
    text="Trie Keyword Suggestion System © 2025",
    font=("Arial", 12)
)
footer.pack(side="bottom", pady=15)

# Chạy chương trình
app.mainloop()