import os 
import shutil 
import uvicorn 
import json
from pathlib import Path
from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

app = FastAPI()
# Tell FastAPI where templates folder is
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Directory for uploads inside static
UPLOAD_FOLDER = "static/upload"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

database_update = {} #Getting the database update 
account_database = {} #Getting the account database
seller_infodb = {} #Getting the seller and buyer information  
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("buyzy.html", {"request": request})
@app.get("/signin",response_class=HTMLResponse)
async def signinpage(request: Request):
     return templates.TemplateResponse("signin.html",{"request":request})
@app.get("/profile/{account}",response_class=HTMLResponse)
async def profile_page(request: Request,account:str):
     return templates.TemplateResponse("profile_page.html",{"request":request,"account_data":account})  
@app.get("/signup",response_class=HTMLResponse)
async def signuppage(request: Request):
     return templates.TemplateResponse("signup.html",{"request":request}) 
@app.post("/database")
async def database_endpoint(request: Request):
     reqdat = await request.json()
     prod_file_path = Path("C:/Users/USER/AppData/Local/Programs/Python/Python38/static/product_database.json")
     # Open the file and load JSON
     prod_db = prod_file_path.open('r', encoding='utf-8')
     productJsonData = json.loads(prod_db.read())
     return productJsonData
@app.post("/update_realdb")
async def updaterealdb(request: Request):
       reqdat = await request.json() #Getting the database request for current update change 
       print("Update database: ",reqdat) #Display update database 
       database_update['title'] = 'สินค้าอิเล็กทรอนิกส์ทั้งหมด' 
       database_update['products'] = [] #Store the product parameter in JSON element 
       '''
       {
                    "id": 106,
                    "name": "Smart Switch",
                    "price": 599,
                    "original_price": 7999,
                    "discount_percent": 18,
                    "popularity_rating": 4.5,
                    "stock_quantity": 140,
                    "image_url": "https://via.placeholder.com/300x200?text=Gaming+Mousepad"
                }
       '''
       payload = reqdat.get('payload') #Get the payload request input 
       database_update['products'].append(payload) #Output database update  
       return database_update 
@app.get("/get_total_db")
async def testdbdata():
      return database_update   
@app.get("/test_javatalk",response_class=HTMLResponse)
async def response_talk(request: Request):
     return templates.TemplateResponse("test_talkjava.html",{"request": request})
@app.post("/send_endpoint")
async def  logindata(request: Request):
     reqdat = await request.json()  
     print(reqdat)
     return reqdat
@app.get("/seller_account",response_class=HTMLResponse)
async def seller_information_form(request: Request):
       return templates.TemplateResponse("seller_info_form.html",{"request":request})   
@app.get("/notify_data",response_class=HTMLResponse)
async def notify_test_verify(request: Request):
       return templates.TemplateResponse("notify_test.html",{"request":request})  
@app.post("/seller_form_input")
async def sellerinputform(request: Request):
      sellerform  = await request.json() #Getting the seller form input JSON 
      print("Seller input form: ",sellerform) #Getting the seller 
      #seller_infodb  
      #{'shop_name': 'Buyzy store', 'phone': '0970762483', 'email': 'kantaphat@hotmail.com', 'seller_type': 'individual', 'tax_id': '421453453453535', 'addess': 'LA ', 'bankaccount': '3453145353535335'}
      email = sellerform.get('email') #Getting the email information 
      if seller_infodb == {}:
             seller_infodb[email] = sellerform #Getting total data store 
      if seller_infodb !={}: 
              if email not in list(seller_infodb):
                         seller_infodb[email] = sellerform 
              if email in list(sellerform):
                         sellerform[email] = sellerform                    
      return sellerform 
@app.get("/seller_info_db")
async def sellerdatabase_information():
      
        return seller_infodb #
@app.get("/orders",response_class=HTMLResponse)
async def ordersdata(request: Request):
         
         return templates.TemplateResponse("orders.html",{"request":request})
@app.get("/manage_products",response_class=HTMLResponse)
async def manages_data(request: Request):
         
         return templates.TemplateResponse("manage_products.html",{"request":request})
@app.get("/sales_today",response_class=HTMLResponse)
async def sales_todaydat(request: Request):
         
         return templates.TemplateResponse("sales_today.html",{"request":request})
@app.get("/shop_profile",response_class=HTMLResponse)
async def shopprofiledata(request: Request):
          
         return templates.TemplateResponse("shop_profile.html",{"request":request})
@app.get("/shipping_info",response_class=HTMLResponse)
async def shopprofiledata(request: Request):
          
         return templates.TemplateResponse("shipping_info.html",{"request":request})

# test_productdata.html
@app.get("/test_productdata",response_class=HTMLResponse)
async def resp_product(request: Request):
     return templates.TemplateResponse("test_productdata.html",{"request": request})
@app.get("/seller_profile",response_class=HTMLResponse)
async def sellerprofile(request: Request):
     return templates.TemplateResponse("manage_products.html",{"request": request})
@app.post("/signin_db")
async def sigindbcheck(request:Request):
       accountcheck = await request.json() #Check the database JSON 
       email = accountcheck.get("email")
       password = accountcheck.get("password") 
       #Checking existing database 
       email_list = list(account_database) #List of the email database 
       #password_list = list(account_database.values()) #List of the value in database 
       print("Getting list of the email and password data and check existing list") 
       if email in email_list:
                passw_realname = account_database.get(email)
                print("Account extraction: ",passw_realname) 
                passwords  = passw_realname.get("password") #Getting the password data 
                realnames = passw_realname.get("realname") #Getting the real name
                print("Password data: ",passwords,realnames) 
                print("Congratulation !!!!!")
                if password == passwords: 
                   #Checking that the user data seller or buyer information is store in database 
                   print("Seller type: ",account_database[email]['user_type'])
                   return {"status":"success","user_type":account_database[email]['user_type']} #Sending return data sucess 
                if password != passwords:
                   return {"status":"warning"} #Sending return data of fail signing in
       else:
          print("Data base not found !")
          return {"status":"warning"} 

@app.post("/account_db")
async def account_databasedat(request: Request):
       accountdata = await request.json()
       email = accountdata.get("email") #Getting email data 
       password = accountdata.get("password") #Getting password data
       realname = accountdata.get("realname") #Getting the real name data 
       user_type = accountdata.get("user_type")
       #print("Input sigup: ",accountdata)
       account_database[email] = {"password":password,"realname":realname,"user_type":user_type}  #Store database back-end 
       print("Account data stored:",account_database)
       return account_database
@app.get("/total_accountdat")
async def total_accountdatabase():
       return account_database      
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_location = f"{UPLOAD_FOLDER}/{file.filename}"

    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {
        "status": "success",
        "filename": file.filename,
        "url": f"/static/upload/{file.filename}"
    }

if __name__ == "__main__":

    uvicorn.run("framework_html:app",host="0.0.0.0",port=8080)
