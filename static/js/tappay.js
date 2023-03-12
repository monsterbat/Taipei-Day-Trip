TPDirect.setupSDK(126863, "app_me7IhP6OtFlPFLLeNmXxd3lusEmHaA8rit01fAC1mEDDPpjBFk9Kf5I94hk1", 'sandbox')
// TPDirect.setupSDK(`${appId}`, `${appKey}`, 'sandbox')
// Display ccv field
let fields = {
    number: {
        // css selector
        element: '#card-number',
        placeholder: '**** **** **** ****'
    },
    expirationDate: {
        // DOM object
        element: document.getElementById('card-expiration-date'),
        placeholder: 'MM / YY'
    },
    ccv: {
        element: '#card-ccv',
        placeholder: 'ccv'
    }
}
TPDirect.card.setup({
    fields: fields,
    styles: {
        // Style all elements
        'input': {
            'color': 'gray'
        },
        // Styling ccv field
        'input.ccv': {
            'font-size': '16px'
        },
        // Styling expiration-date field
        'input.expiration-date': {
            'font-size': '16px'
        },
        // Styling card-number field
        'input.card-number': {
            'font-size': '16px'
        },
        // style focus state
        ':focus': {
            // 'color': 'black'
        },
        // style valid state
        '.valid': {
            'color': 'green'
        },
        // style invalid state
        '.invalid': {
            'color': 'red'
        },
        // Media queries
        // Note that these apply to the iframe, not the root window.
        '@media screen and (max-width: 400px)': {
            'input': {
                'color': 'orange'
            }
        }
    },
    // 此設定會顯示卡號輸入正確後，會顯示前六後四碼信用卡卡號
    isMaskCreditCardNumber: true,
    maskCreditCardNumberRange: {
        beginIndex: 6,
        endIndex: 11
    }
})

async function getBookingData(){
    return fetch(`/api/booking`,{
        method:"GET",
    }).then(function(response){
        return response.json();
    }).then(function(data){
        return data
    })
}
 
async function getUserData(){
    return fetch(`/api/user/auth`,{
        method:"GET",
    }).then(function(response){
        return response.json();
    }).then(function(data){
        return data
    })
}

let payButton = document.getElementById("payBlock")
payButton.addEventListener("click",onSubmit)

function onSubmit(event) {
    let processFilter = document.getElementById("processFilter")
    let processInf = document.getElementById("processInf")
    processFilter.style.display = "flex"
    processInf.style.display = "flex"
    event.preventDefault()

    // 取得 TapPay Fields 的 status
    const tappayStatus = TPDirect.card.getTappayFieldsStatus()

    // Get prime
    TPDirect.card.getPrime(async(result) => {
        if (result.status !== 0) {
            alert('get prime error ' + result.msg)
            return
        }
        // alert('get prime 成功，prime: ' + result.card.prime)
        let bookingData = await getBookingData() 
        let userData = await getUserData()
        let userNameShow = userData.data.name
        let userEmailShow = userData.data.email
        let userIdShow = userData.data.id
        let bookingIdShow = bookingData.data.attraction.id
        let bookingNameShow = bookingData.data.attraction.name
        let bookingAddressShow = bookingData.data.attraction.address
        let bookingImgShow = bookingData.data.attraction.image
        let bookingDateShow = bookingData.data.date
        let bookingTimeShow = bookingData.data.time
        let bookingPriceShow = bookingData.data.price
        let phoneInput = document.getElementById("phoneInput").value
        data = {
            "prime": result.card.prime,
            "order": {
              "price": bookingPriceShow,
              "trip": {
                "attraction": {
                  "id": bookingIdShow,
                  "name": bookingNameShow,
                  "address": bookingAddressShow,
                  "image": bookingImgShow
                },
                "date": bookingDateShow,
                "time": bookingTimeShow
              },
              "contact": {
                "name": userNameShow,
                "email": userEmailShow,
                "phone": phoneInput
              }
            }
        }

        fetch(`/api/orders`,{
            method:"POST",
            body:JSON.stringify(data),
            headers:new Headers({
                "Content-Type":"application/json"
            })
        }).then(function(response){
            return response.json();
        }).then(function(data){
            if (data.error == true){
                return alert(data.message)
            }
            window.location.href = `/thankyou?number=${data.data.number}`
            return data
        })

    })
}