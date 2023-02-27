# IntroductionToAIBTL1

## Chuẩn bị Thư Viện
chạy lệnh sau để cài đặt thư viện:
```
    pip install -r requirement.txt
```
## Về luật chơi
Tham khảo tại: [game link](https://www.coolmathgames.com/0-bloxorz)
<br>
Một số lưu ý về mô phỏng:
- một nút nhẹ là một nút chỉ cần nằm trên nút đó là có thể kích hoạt (trong mô phỏng là dạng hình tròn)
- một nút nặng là một nút phải đứng trên nút đó là có thể kích hoạt (trong mô phỏng là dấu X trên ô)
- Trong trò chơi trên có nút tách làm 2 nhưng trong mô phỏng này không có và coi như không tồn tại testcasse có nút đó

## Không gian trạng thái
Ta thấy để giải bài toán trò chơi này, ta cần quan tâm ba thành phần sau:
- Bàn chơi (board)
- Khối di chuyển (Cube) (đúng ra phải đặt là box mà lỡ đặt cube rồi nên lười sửa)
- Các nút (Button)
Vì vậy ta có không gian trạng thái sau:
### State
Đối với khối di chuyển (Cube), vì ta thấy 1 cube gồm 2 cube nhỏ hơn nên 1 cube sẽ được định nghĩa gồm 2 khối lập phương nhỏ hơn. Vậy state của 1 cube là tọa độ của 2 khối lập phương đó theo dạng **(hàng,cột)** với kiểu dữ liệu **tuple**. Trong đó **firstCube** và **secondCube** lần lượt chứa tọa độ của từng khối lập phương và tuân theo quy tắc sau:
- Nếu khối di chuyển đang nằm thẳng đứng **firstCube == secondCube**
- Nếu khối di chuyển nằm ngang theo chiều cùng 1 hàng, tọa độ cột của **firstCube** phải nhỏ hơn **secondCube**
- Nếu khối di chuyển nằm dọc theo chiều cùng 1 cột, tọa đồ hàng của của **firstCube** phải nhỏ hơn **secondCube**
ví dụ về tọa đọ hợp lệ:
```
    firstCube = (1,1)
    secondCube = (1,1)
    ###
    firstCube = (1,1)
    secondCube = (1,2)  ### Ngược lại là không hợp lệ
    ###
    firstCube = (1,1)
    secondCube = (2,1)  ### ngược lại là không hợp lệ
```
Đối với bàn chơi (board), board là một **dictionary** trong python với các key là tọa độ **(hàng, cột)** của ô nào đó với key ở kiểu **tuple**, value của mỗi key là một số **int**. Trong đó value gồm:
- 0 ứng với không có ô đó
- 1 ứng với ô yếu (ô không được đứng trên đó, hay số khối lập phương nhỏ có tọa độ tại ô đó tối đa là 1)
- 2 ứng với ô bình thường (ô có thể đứng trên đó, hay số khối lập phương nhỏ có tọa độ tại ô đó tối đa là 2)
- 3 ứng vô vị trí đích (vị trí ta muốn đứng trên đó)
ví dụ:
<br>

Đây là một kiểu của board:
```
{ (0,0):2, (0,1):1, (0,2):1, (0,3):2, (0,4):3, (0,5):2, (0,6):0}
```
Đây là hình ảnh mô phỏng board trên: 
<br>

![alt](https://i.imgur.com/OA7oB4y.png)
<br>

Đối với các nút bấm (button), các nút bấm được chứa trong buttonList là một **Dictionary** với key là tọa độ đặt nút bấm đó. Kiểu của key là **tuple**, value tương ứng là một **List** vói phần tử đầu là kiểu của nút bấm (1 cho nút chỉ cần 1 khối lập phương để kích hoạt, 2 cho nút cần 2 khối lập phương phương để kích hoạt). Phần tử thứ hai là một **List** chứ các tuple là tọa độ các ô sẽ xuất hiện (nếu chưa tồn tại) hoặc mất đi (nếu đã tồn tại) khi bấm nút đó.
<br>

ví dụ về list các nút bấm:
```
    {(2,2):[2,[(5,9),(5,10)]], (1,2):[1,[(0,4)]]}
```
Trong các file cần hiện thực lời giải bằng cách giải thuật *(MonterCarLoTreeSearch.py, BlindSearch.py, A_star.py)* Đều đã được truyền vào các giá trị board, firstCube, secondCube và buttonList theo đúng định dạng trên.
Yêu cầu các phương thức **solve()** trong các lớp trên phải trả về kết quả là một **list** mà mỗi phần tử trong **list** đó là một **list** chứa 2 **tuple** tương ứng của **firstCube** và **secondCube** dẫn tới lời giải 
### Input TestCase
Một testcase hợp lệ trong file có dạng sau:
```
TESTCASE
[
    {}, ### này là dictionary của board
    [( , ),( , )], ### vị trí bắt đầu của cái khối đó
    {} #### Dictionary các nút bấm
]
END
```
Ví dụ:
```
TESTCASE2
[
{(0,0):2,(0,1):2,(0,2):2,
(1,0):2,(1,1):2,(1,2):2,(1,3):2,(1,4):2,(1,5):2,
(2,0):2,(2,1):2,(2,2):2,(2,3):2,(2,4):2,(2,5):2,(2,6):2,(2,7):2,(2,8):2,
(3,1):2,(3,2):2,(3,3):2,(3,4):2,(3,5):2,(3,6):2,(3,7):2,(3,8):2,(3,9):2,
(4,5):2,(4,6):2,(4,7):3,(4,8):2,(4,9):2,
(5,6):2,(5,7):2,(5,8):2},
[(1,1),(1,1)],
{(2,2):[2,[(5,9),(5,10)]],
(1,2):[1,[(0,4)]]}
]
END
```
Kết quả mô phỏng:
<br>

![alt](https://i.imgur.com/z2ldeYV.png)

```