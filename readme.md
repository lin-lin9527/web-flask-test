'/':首頁
'/api/register':創帳號密碼
'/api/admin':查詢使用者資料
'/api/user/delete/id=':刪除單獨資料
'/api/upload':上傳圖片
'/api/update':更新密碼
'/api/user/<string:username>/delete' :指定user資料隱藏
'/api/user/<string:username>/reset' :指定user資料還原
'/api/user/<string:username>':單獨資料查詢
'/api/message':email
'/api/download/csv':csv 下載
'/api/download/json':json 下載

資料庫遷移

python .py db init
python .py db migrate
pyhthon .py db upgrade


