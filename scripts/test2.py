# import pygame
# import time

# # Khởi tạo Pygame
# pygame.init()

# # Kích thước cửa sổ
# SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
# screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
# pygame.display.set_caption("Text Reveal Effect with Word Wrap")

# # Màu sắc
# BLACK = (0, 0, 0)
# WHITE = (255, 255, 255)

# # Phông chữ
# font = pygame.font.Font(None, 36)

# # Nội dung hội thoại
# text = "Hello, this is a sample text appearing one character at a time! It will automatically wrap to the next line when the text exceeds the width of the box."
# text_speed = 50  # Tốc độ xuất hiện ký tự (ký tự/giây)

# # Vị trí hộp thoại
# text_box = pygame.transform.scale(pygame.image.load("data/images/UI/dialog box big.png"), (800, 200))
# text_box_rect = text_box.get_rect()
# line_spacing = 5  # Khoảng cách giữa các dòng

# # Biến hỗ trợ
# clock = pygame.time.Clock()
# running = True
# start_time = time.time()
# displayed_text = ""

# # Hàm để tự động xuống dòng
# def wrap_text(text, font, max_width):
#     lines = []
#     words = text.split(" ")
#     current_line = ""

#     for word in words:
#         test_line = f"{current_line} {word}".strip()
#         if font.size(test_line)[0] <= max_width:
#             current_line = test_line
#         else:
#             lines.append(current_line)
#             current_line = word
#     if current_line:
#         lines.append(current_line)
#     return lines

# # Hàm để cập nhật văn bản theo thời gian
# def update_text(text, elapsed_time, speed):
#     chars_to_show = int(elapsed_time * speed)
#     return text[:chars_to_show]

# # Vòng lặp chính
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # Thời gian đã trôi qua
#     elapsed_time = time.time() - start_time

#     # Cập nhật văn bản hiển thị
#     displayed_text = update_text(text, elapsed_time, text_speed)

#     # Tự động chia nhỏ văn bản theo chiều rộng hộp thoại
#     wrapped_lines = wrap_text(displayed_text, font, text_box_rect.width - 20)

#     # Vẽ nền
#     screen.fill(BLACK)

#     # Vẽ hộp thoại
#     screen.blit(text_box, (0, 200))

#     # Vẽ từng dòng văn bản
#     for i, line in enumerate(wrapped_lines):
#         text_surface = font.render(line, True, BLACK)
#         screen.blit(text_surface, (text_box_rect.x + 10, text_box_rect.y + 10 + i * (font.get_linesize() + line_spacing)))

#     # Cập nhật màn hình
#     pygame.display.flip()

#     # Giới hạn FPS
#     clock.tick(30)

# pygame.quit()


text = "hello mate, my name is Ron"
print(text.split(" "))
print(text.strip())