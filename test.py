# import webview

# # Hàm này sẽ được gọi từ cửa sổ WebView
# def click_point():
#     # Đoạn mã JavaScript để click vào một phần tử (theo ID hoặc class)
#     js_code = '''
#     var element = document.elementFromPoint(100, 200); // Tọa độ 100, 200 trên trang
#     if (element) {
#         element.click();  // Gọi sự kiện click lên phần tử tại vị trí này
#     }
#     '''
#     # Thực thi JavaScript
#     window.evaluate_js(js_code)

# # Tạo cửa sổ WebView
# window = webview.create_window('WebView với thao tác click', 'nguyen_trung_truc.html')

# # Chạy cửa sổ WebView và kích hoạt thao tác click sau 5 giây (có thể thay đổi)
# webview.start(click_point, window)
import webview

# Define a class to handle the received coordinates
class Api:
    def send_coordinates(self, coords):
        start_coords, end_coords = coords
        print(f"Start Coordinates: {start_coords}")
        print(f"End Coordinates: {end_coords}")
        # Here you can add code to process the coordinates, e.g., calculate the shortest path

# Create an instance of the API class
api = Api()

# Create a WebView window and expose the API
#window = webview.create_window('WebView with Map Click', 'nguyen_trung_truc.html', js_api=api)
window = webview.create_window('WebView with Map Click', 'test.html', js_api=api)

# Start the WebView
webview.start(debug=True, http_server=True)