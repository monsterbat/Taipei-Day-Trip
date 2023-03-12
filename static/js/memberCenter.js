let mainDiv = document.getElementById("main")
let anchorDiv = document.getElementById("anchor")



// Get bookin inf
async function getBookingData(){
    return fetch(`/api/booking`,{
        method:"GET",
    }).then(function(response){
        return response.json();
    }).then(function(data){
        return data
    })
}
// Get user inf
async function getUserData(){
    return fetch(`/api/user/auth`,{
        method:"GET",
    }).then(function(response){
        return response.json();
    }).then(function(data){
        return data
    })
}

// Get orders inf
async function getOrdersHistoryData(userId){
    console.log("R",userId)
    return fetch(`/api/orders/history/${userId}`,{
        method:"GET",
    }).then(function(response){
        return response.json();
    }).then(function(data){
        return data
    })
}

// Change user inf
async function changeUserInf(data){
    return fetch(`/api/user/auth`,{
        method:"PATCH",
        body:JSON.stringify(data),
        headers:new Headers({
            "Content-Type":"application/json"
        })
    }).then(function(response){
        return response.json();
    }).then(function(data){ 
        return data
    });
}

// creat element
function createElement(appendBlock, elementStyle, elementName, elementText = null){
    element = document.createElement(elementStyle);
    element.setAttribute("id",elementName);
    element.setAttribute("class",elementName);    
    if (elementStyle == "img"){
        element.src = elementText;
    }
    else{
        element.textContent = elementText;
    }
    appendBlock.appendChild(element);
    globalThis.elementName = document.getElementById(elementName)
}
// Replace element
function replaceElement(originalElement, newElementStyle, newElementName, elementText = null){
    originalElementBlock = document.getElementById(originalElement)
    
    element = document.createElement(newElementStyle);
    element.setAttribute("id",newElementName);
    element.setAttribute("class",newElementName);    
    if (newElementStyle == "img"){
        element.src = elementText;
    }
    if (newElementStyle == "input"){
        element.type = 'text';
        element.setAttribute("value",elementText);
    }
    else{
        element.textContent = elementText;
    }
    originalElementBlock.parentNode.replaceChild(element,originalElementBlock);

    globalThis.newElementName = document.getElementById(newElementName)
}

createUserInf()
async function createUserInf(){
    let userData = await getUserData()
    console.log(userData)
    let userName = userData.data.name
    let userMail = userData.data.email
    let userId = userData.data.id
    globalThis.userId = userId
    globalThis.userName = userName
    globalThis.userMail = userMail
    console.log(userId)
    // Fix title
    // 1-0      userCenterTitle
    createElement(mainDiv,"div","userCenterTitle","會員中心")


    // Choose History or user list
    // 1-C      listChangeBlock
    createElement(mainDiv,"div","listChangeBlock")
    // 1-C-1    changeTouser
    createElement(listChangeBlock,"div","changeToUser","基本資料")
    // 1-C-2    changeToHistory
    createElement(listChangeBlock,"div","changeToHistory","歷史訂單")
    changeToHistory.style.backgroundColor = "#fafafafa"
    // User Img and Name
    // 1-1      userIconAndName
    createElement(mainDiv,"section","userIconAndName")
    // 1-1-1    userIconBlock
    createElement(userIconAndName,"div","userIconBlock")
    // 1-1-1-1  userIcon
    createElement(userIconBlock,"img","userIcon", "../static/image/profile_pic_icon.png")
    // 1-1-1-2  userEditIcon
    createElement(userIconBlock,"div","userEditIconBlock")
    createElement(userEditIconBlock,"img","userEditIcon", "../static/image/Edit_icon.png")
    createElement(userIconBlock,"div","userFinishIconBlock")
    createElement(userFinishIconBlock,"img","userFinishIcon", "../static/image/ok_icon.png")
    userFinishIconBlock.style.display = "none"
    
    // 1-1-2    userNameBlock
    createElement(userIconAndName,"div","userNameBlock")
    // 1-1-2-1  userName
    createElement(userNameBlock,"div","userName",userName)
    // 1-1-2-2  userNameEdit
    createElement(userNameBlock,"div","userNameEditBlock")
    createElement(userNameEditBlock,"img","userNameEdit", "../static/image/Edit_icon.png")
    createElement(userNameBlock,"div","userNameFinishBlock")
    createElement(userNameFinishBlock,"img","userNameFinish", "../static/image/ok_icon.png")
    userNameFinishBlock.style.display = "none"


    // user inf
    // 1-2      userMailAndPassword
    createElement(mainDiv,"section","userMailAndPassword")

    // 1-2-1    userMailTitle
    createElement(userMailAndPassword,"div","userMailTitle","會員信箱：")
    // 1-2-2    userMailBlock
    createElement(userMailAndPassword,"div","userMailBlock")
    // 1-2-2-1  userMail
    createElement(userMailBlock,"div","userMail",userMail)
    // 1-2-2-2  userMailEdit
    createElement(userMailBlock,"div","userMailEditBlock")
    createElement(userMailEditBlock,"img","userMailEdit", "../static/image/Edit_icon.png")
    createElement(userMailBlock,"div","userMailFinishBlock")
    createElement(userMailFinishBlock,"img","userMailFinish", "../static/image/ok_icon.png")
    userMailFinishBlock.style.display = "none"


    // 1-2-3    userPasswordTitle
    createElement(userMailAndPassword,"div","userPasswordTitle","會員密碼：")
    // 1-2-4    userPasswordBlock
    createElement(userMailAndPassword,"div","userPasswordBlock")
    // 1-2-4-1  userPassword
    createElement(userPasswordBlock,"div","userPassword","******")
    console.log(userPassword)
    // 1-2-4-2  userPasswordEdit
    createElement(userPasswordBlock,"div","userPasswordEditBlock")
    createElement(userPasswordEditBlock,"img","userPasswordEdit", "../static/image/Edit_icon.png")
    createElement(userPasswordBlock,"div","userPasswordFinishBlock")
    createElement(userPasswordFinishBlock,"img","userPasswordFinish", "../static/image/ok_icon.png")
    userPasswordFinishBlock.style.display = "none"

    // 1-2-5    newPassword
    createElement(userMailAndPassword,"div","userNewPasswordBlock")
    createElement(userNewPasswordBlock,"input","newPassword")
    userNewPasswordBlock.style.display = "none"
    // 1-2-6    newPasswordCheck
    createElement(userMailAndPassword,"div","userNewPasswordCheckBlock")
    createElement(userNewPasswordCheckBlock,"input","newPasswordCheck")
    userNewPasswordCheckBlock.style.display = "none"
    

    // Booking history
    let userOrdersHistory = await getOrdersHistoryData(userId)
    dataQty = Object.keys(userOrdersHistory).length
 

    // 1-3      orderHistory
    createElement(mainDiv,"section","orderHistory")
    // // 1-3-1    orderHistoryTitle
    // createElement(orderHistory,"div","orderHistoryTitle","歷史訂單")
    // noHistoryData
    if(dataQty == 0){
        // 1-3-2N   NoData
        createElement(orderHistory,"div","noHistoryDataBlock")
        createElement(noHistoryDataBlock,"div","noHistoryData","無資料")
    }
    for (let i = 0; i<dataQty; i++){
        console.log("123")
        let attraction_id = userOrdersHistory[i]["attraction_id"]
        let attraction_name = userOrdersHistory[i]["attraction_name"]
        let attraction_address = userOrdersHistory[i]["attraction_address"]
        let attraction_image = userOrdersHistory[i]["attraction_image"]
        let order_date = userOrdersHistory[i]["order_date"]
        let order_time = userOrdersHistory[i]["order_time"]
        let order_number = userOrdersHistory[i]["order_number"]
        let pay_status = userOrdersHistory[i]["pay_status"]


        // 1-3-2    orderHistoryList
        createElement(orderHistory,"div",`orderHistoryList${i}`)
        eval(`orderHistoryList${i}`).setAttribute("class","orderHistoryList"); 
        // 1-3-2-1  orderHistoryNumber
        createElement(eval(`orderHistoryList${i}`),"div",`orderHistoryNumber${i}`,i+1)
        eval(`orderHistoryNumber${i}`).setAttribute("class","orderHistoryNumber");
        // 1-3-2-2  orderHistoryImg
        createElement(eval(`orderHistoryList${i}`),"div",`orderHistoryImgBlock${i}`)
        eval(`orderHistoryImgBlock${i}`).setAttribute("class","orderHistoryImgBlock");

        createElement(eval(`orderHistoryImgBlock${i}`),"img",`orderHistoryImg${i}`,attraction_image)
        eval(`orderHistoryImg${i}`).setAttribute("class","orderHistoryImg");
        // 1-3-2-3  orderHistoryDetail
        createElement(eval(`orderHistoryList${i}`),"div",`orderHistoryDetail${i}`)
        eval(`orderHistoryDetail${i}`).setAttribute("class","orderHistoryDetail");
        // 1-3-2-3-1 orderHistoryAttraction
        createElement(eval(`orderHistoryDetail${i}`),"div",`orderHistoryAttractionTitle${i}`,"景點名稱： "+attraction_name)
        eval(`orderHistoryAttractionTitle${i}`).setAttribute("class","orderHistoryAttractionTitle");
        // 1-3-2-3-2 orderHistoryDate
        createElement(eval(`orderHistoryDetail${i}`),"div",`orderHistoryDateTitle${i}`,"預約日期： "+order_date)
        eval(`orderHistoryDateTitle${i}`).setAttribute("class","orderHistoryDateTitle");
        // 1-3-2-3-3 orderHistoryTime
        createElement(eval(`orderHistoryDetail${i}`),"div",`orderHistoryTimeTitle${i}`,"預約時間： "+order_time)
        eval(`orderHistoryTimeTitle${i}`).setAttribute("class","orderHistoryTimeTitle");
        // 1-3-2-3-4 orderHistoryOrderNumber
        createElement(eval(`orderHistoryDetail${i}`),"div",`orderHistoryOrderNumberTitle${i}`,"訂單編號： "+order_number)
        eval(`orderHistoryOrderNumberTitle${i}`).setAttribute("class","orderHistoryOrderNumberTitle");
        // 1-3-2-3-5 orderHistoryPayment
        createElement(eval(`orderHistoryDetail${i}`),"div",`orderHistoryPaymentTitle${i}`,"付款狀態： "+pay_status)
        eval(`orderHistoryPaymentTitle${i}`).setAttribute("class","orderHistoryPaymentTitle");
    }
    orderHistory.style.display = "none"

    // Update finish
    createElement(mainDiv,"div","finishFilter")
    createElement(mainDiv,"div","finishBlockBorder")
    createElement(finishBlockBorder,"div","finishBlock")
    createElement(finishBlock,"div","finishHint")
    finishHint.textContent = "";
    createElement(finishBlock,"div","finishOk","確定")

    clickFunction()
}

// changeToHistory.addEventListener("click",test)
function clickFunction(){
    changeToHistory.addEventListener("click",clickToHistory)
    changeToUser.addEventListener("click",clickToUser)
    userEditIconBlock.addEventListener("click",clickToEditUserIcon)
    userFinishIconBlock.addEventListener("click",clickFinishUserIcon)
    userNameEditBlock.addEventListener("click",clickToEditUserName)
    userNameFinishBlock.addEventListener("click",clickToFinishUserName)
    userMailEditBlock.addEventListener("click",clickToEditUserMail)
    userMailFinishBlock.addEventListener("click",clickToFinishUserMail)
    userPasswordEditBlock.addEventListener("click",clickToEditUserPassword)
    userPasswordFinishBlock.addEventListener("click",clickToFinishUserPassword)
    finishOk.addEventListener("click",clickToCloseWindow)
}


async function clickToHistory(){
    userMailAndPassword.style.display = "none"
    orderHistory.style.display = "flex"
    changeToHistory.style.backgroundColor = "#f5f5f5f5"
    changeToUser.style.backgroundColor = "#fafafafa"

}

async function clickToUser(){
    userMailAndPassword.style.display = "flex"
    orderHistory.style.display = "none"
    changeToHistory.style.backgroundColor = "#fafafafa"
    changeToUser.style.backgroundColor = "#f5f5f5f5"
}
// ------  userIcon Edit
async function clickToEditUserIcon(){
    userEditIconBlock.style.display = "none"
    userFinishIconBlock.style.display = "flex"
}
async function clickFinishUserIcon(){
    userEditIconBlock.style.display = "flex"
    userFinishIconBlock.style.display = "none"
}
// ------  Name Edit
async function clickToEditUserName(){
    userNameEditBlock.style.display = "none"
    userNameFinishBlock.style.display = "flex"

    replaceElement("userName","input","newUserName",userName)
}
async function clickToFinishUserName(){
    newUserNameVaule = newUserName.value
    replaceElement("newUserName","div","userName",newUserNameVaule)
    if(newUserNameVaule != userName){
        data = {
            "userId":userId,
            "newUserName":newUserNameVaule,
            "newUserMail":null,
            "oriUserPassword":null,
            "newUserPassword":null
        }
        requestMsg = await changeUserInf(data)
        globalThis.userName = newUserNameVaule
        finishHint.textContent = requestMsg.message;
    }
    if(newUserNameVaule == userName){
        finishHint.textContent = "相同使用者名稱";
    }
    else{
        finishHint.textContent = "變更失敗";
    }
    finishFilter.style.display = "flex"
    finishBlockBorder.style.display = "flex"
    userNameEditBlock.style.display = "flex"
    userNameFinishBlock.style.display = "none"
}

// ------ Mail Edit
async function clickToEditUserMail(){
    userMailEditBlock.style.display = "none"
    userMailFinishBlock.style.display = "flex"
    replaceElement("userMail","input","newUserMail",userMail)
    userMailBlock.style.borderStyle = "solid"
    userMailBlock.style.borderWidth = "1px"

}
async function clickToFinishUserMail(){
    newUserMailVaule = newUserMail.value
    console.log("newUserMailVaule",newUserMailVaule)
    replaceElement("newUserMail","div","userMail",newUserMailVaule)
    if(newUserMailVaule != userMail){
        data = {
            "userId":userId,
            "newUserName":null,
            "newUserMail":newUserMailVaule,
            "oriUserPassword":null,
            "newUserPassword":null
        }
        requestMsg = await changeUserInf(data)
        globalThis.userMail = newUserMailVaule
        finishHint.textContent = requestMsg.message;
    }
    if(newUserMailVaule == userMail){
        finishHint.textContent = "相同使用者信箱";
    }
    else{
        finishHint.textContent = "變更失敗";
    }
    finishFilter.style.display = "flex"
    finishBlockBorder.style.display = "flex"
    userMailBlock.style.borderStyle = "none"
    userMailEditBlock.style.display = "flex"
    userMailFinishBlock.style.display = "none"
}
// ------ Password Edit
async function clickToEditUserPassword(){
    userPasswordEditBlock.style.display = "none"
    userPasswordFinishBlock.style.display = "flex"
    replaceElement("userPassword","input","oriUserPassword","")
    oriUserPassword.setAttribute("type","password");
    oriUserPassword.setAttribute("placeholder","請輸入原本密碼");
    newPassword.setAttribute("placeholder","請輸入新密碼");
    newPassword.setAttribute("type","password");
    newPasswordCheck.setAttribute("placeholder","再次輸入新密碼");
    newPasswordCheck.setAttribute("type","password");
    userNewPasswordBlock.style.display = "flex"
    userNewPasswordCheckBlock.style.display = "flex"
}
async function clickToFinishUserPassword(){
    newPasswordValue = newPassword.value
    newPasswordCheckValue = newPasswordCheck.value
    oriUserPasswordValue = oriUserPassword.value
    // Check password    
    replaceElement("oriUserPassword","div","userPassword","******")

    if(newPasswordValue !="" && newPasswordValue == newPasswordCheckValue){
        if(newPasswordValue != oriUserPasswordValue){
            data = {
                "userId":userId,
                "newUserName":null,
                "newUserMail":null,
                "oriUserPassword":oriUserPasswordValue,
                "newUserPassword":newPasswordValue
            }
            requestMsg = await changeUserInf(data)
            if (requestMsg.ok){
                finishHint.textContent = requestMsg.message;
            }
            if (requestMsg.error){
                finishHint.textContent = requestMsg.message;
            }
        }
    }
    else{
        if (oriUserPasswordValue == newPasswordValue){
            finishHint.textContent = "相同密碼";
        }
        if (newPasswordValue != newPasswordCheckValue){
            finishHint.textContent = "新密碼兩次輸入不一致";
        }
        if (newPasswordValue == ""){
            finishHint.textContent = "新密碼請勿輸入空白";
        }
        if (oriUserPasswordValue == ""){
            finishHint.textContent = "請輸入原始密碼";
        }
        else{
            finishHint.textContent = "變更失敗";
        }
    }
    finishFilter.style.display = "flex"
    finishBlockBorder.style.display = "flex"
    userPasswordEditBlock.style.display = "flex"
    userPasswordFinishBlock.style.display = "none"
    userNewPasswordBlock.style.display = "none"
    userNewPasswordCheckBlock.style.display = "none"
}

async function clickToCloseWindow(){
    finishFilter.style.display = "none"
    finishBlockBorder.style.display = "none"
}

function test(){
    console.log(changeToHistory)
}