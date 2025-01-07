import pandas as pd
import matplotlib.pyplot as plt

# Đọc dữ liệu từ file CSV
df = pd.read_csv('DonHang.csv')

# Xem trước dữ liệu
print("Trước khi làm sạch:")
print(df.head())

# Bước 1: Xử lý các giá trị thiếu bằng cách thay thế chúng với giá trị mặc định
# Thay thế giá trị thiếu trong cột 'total_amount' bằng 0 và 'status' bằng 'Chưa có'
df['total_amount'] = df['total_amount'].fillna(0)  # Thay giá trị thiếu bằng 0
df['status'] = df['status'].fillna('Chưa có')  # Thay giá trị thiếu bằng 'Chưa có'
df['description'] = df['description'].fillna('Chưa có mô tả')  # Thay giá trị thiếu trong mô tả

# Bước 2: Chỉnh sửa cột 'status' bằng cách thay thế các trạng thái viết tắt hoặc lỗi
df['status'] = df['status'].replace({
    'ĐG': 'Đã Giao',
    'Đã Hủy': 'Đã Hủy',
    'Đang Giao': 'Đang Giao',
    'Chờ Xử Lý': 'Chờ Xử Lý',
    'CXL': 'Chờ Xử Lý'
})

# Bước 3: Chỉnh sửa cột 'description' để loại bỏ khoảng trắng thừa
df['description'] = df['description'].str.strip()

# Xem dữ liệu sau khi làm sạch
print("Sau khi làm sạch:")
print(df.head())

# Lưu lại DataFrame đã làm sạch vào file CSV mới
df.to_csv('cleaned_order.csv', index=False)
# Bước 1: Tính tổng doanh thu cho mỗi khách hàng (customerid)
customer_revenue = df.groupby('customerid')['total_amount'].sum().reset_index()

# Bước 2: Sắp xếp khách hàng theo tổng doanh thu giảm dần
customer_revenue = customer_revenue.sort_values(by='total_amount', ascending=False)

# Bước 3: Lọc ra 5 khách hàng có doanh thu cao nhất
top_5_customers = customer_revenue.head(5)

# Bước 4: Vẽ biểu đồ
plt.figure(figsize=(10, 6))
bars = plt.bar(top_5_customers['customerid'], top_5_customers['total_amount'], color='skyblue')

# Thêm giá trị doanh thu lên trên các cột
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height:,.0f}', 
             ha='center', va='bottom', fontsize=10)

# Chỉnh sửa các thông số biểu đồ
plt.xlabel('Mã khách hàng')
plt.ylabel('Doanh thu (VND)')
plt.title('Top 5 khách hàng mua nhiều nhất (doanh thu)')
plt.xticks(rotation=45)
plt.tight_layout()

# Hiển thị biểu đồ
plt.show()



# Bước 1: Tính số lượng mỗi loại sách (dựa trên cột 'description')
book_sales = df['description'].value_counts()

# Bước 2: Tính tỉ lệ bán cho từng loại sách
sales_ratio = book_sales / book_sales.sum() * 100

# Bước 3: Vẽ biểu đồ tròn (pie chart) thể hiện tỉ lệ bán
plt.figure(figsize=(8, 8))
plt.pie(sales_ratio, labels=sales_ratio.index, autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
plt.title('Tỉ lệ bán các loại sách')

# Hiển thị biểu đồ
plt.axis('equal')  # Đảm bảo biểu đồ tròn có dạng tròn
plt.show()



# Bước 2: Nhóm theo ngày và tình trạng, tính số lượng đơn hàng cho mỗi tình trạng vào mỗi ngày
status_per_day = df.groupby([df['Order_date'], 'status']).size().unstack(fill_value=0)

# Bước 3: Vẽ biểu đồ cột lồng nhau
status_per_day.plot(kind='bar', figsize=(10, 6), width=0.8, stacked=False, colormap='tab20')

# Cải thiện hiển thị
plt.title('Tình trạng đơn hàng theo ngày')
plt.xlabel('Ngày')
plt.ylabel('Số lượng đơn hàng')
plt.xticks(rotation=45)
plt.tight_layout()

# Hiển thị biểu đồ
plt.show()