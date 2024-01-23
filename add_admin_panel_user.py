import os
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from dotenv import load_dotenv

load_dotenv()

URL = os.getenv("DATABASE_URL_PS", "postgresql+psycopg2://postgres@localhost/legadrop")

engine = create_engine(URL, echo=True)

user_param = {
    "login": "admin1",
    "password": r"afA)B#xtZe@rHv#ea6@S",
    "token": r".|;>11TK.yqsG8+RFjs1?=Yg=63laQFBQ2qX557):YFpx]R*@)39j6?[PZ!c@3%Pa<M|)zauGfs;6|S4Khr(mnq=([A+wg>XX1y;|E$i_t?@X9uo;?$W+%4(ZCY}m)2AIKU@X&j<S)wsiOp@IDgN9_e,&.v3A=hL5liqR-?bB50jKZ-Y{0KP8IdZEol38vcXRHLnat#(Vx;gabN5?cW92=H.dK[iBeWtwkk+GMLPa:!9}+x?9|%:HKSb[,/]Y4bgMIdt6b8OOdEh+uoA/ZzJalNe[tu#$k#?fBW#bq!mg;V$Dx^V^zGzW7Y)j/tQT&ik4uNN,,=^B>vlwE6zS$2zwAui,<C1h*ryuy=I_4_08z6DCbBIi_YoI+3x?*vjW#{j2p]0djQzd-aFL}||X5uwy3+8Ii@w.hCe[T|}aD[l=(}:7MHD2B:fD;mSrOP]Ps9srH7M#;F6<@AvI.}bcgive=^aR0y&,W.O?$y/.loYSl@iQyJab({fe56_-$2SL72*",
}

from models.models import AdminPanelUser

with Session(autoflush=True, bind=engine) as session:
    user = AdminPanelUser(
        login=user_param["login"],
        password=user_param["password"],
        token=user_param["token"],
    )
    session.add(user)
    session.commit()
    print(user.id)
    print(user.login)
    print(user.password)
    print(user.token)
