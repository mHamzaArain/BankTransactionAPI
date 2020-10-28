# Bank Transaction API

| Resources        | Protocol | Path      | Parameter                                                     | Status code                                                  | Description                                   |
|------------------|----------|-----------|---------------------------------------------------------------|--------------------------------------------------------------|-----------------------------------------------|
| Register<br>user | POST     | /register | username: String<br>pw: String                                | 200 OK<br>301 User already exist<br>302                      | Register a user                               |
| Add money        | POST     | /add      | username: String<br>pw: String<br>amount: float               | 200 OK<br>301 Invalid user<br>302 Invalid password           | Classify image                                |
| Transfer money   | POST     | /transfer | username: String<br>pw: String<br>to: String<br>amount: float | 200 OK<br>301 Invalid username<br>302 Invalid admin_password | Increase/decrease the limit of tokens of user |
| Check balance    | POST     | /balance  | username: String<br>pw: String                                | 200 OK<br>301 Invalid username<br>302 Invalid admin_password | Increase/decrease the limit of tokens of user |
| Take loan        | POST     | /takeLoan | username: String<br>pw: String<br>amount: float               | 200 OK<br>301 Invalid username<br>302 Invalid admin_password | Increase/decrease the limit of tokens of user |
| Pay loan         | POST     | /payLoan  | username: String<br>pw: String<br>amount: float               | 200 OK<br>301 Invalid username<br>302 Invalid admin_password | Increase/decrease the limit of tokens of user |
