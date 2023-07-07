function testCurrentURL() {
    let currentURL = window.location.href
    let pathname = window.location.pathname;
    console.log(currentURL)
    if (currentURL.includes('register')) {
        $(".register-content").show()
        $(".login-content").hide()
        $(".modify-password").hide()
        $(".reset-password").hide()
    } else if (currentURL.includes('login')) {
        $(".login-content").show()
        $(".register-content").hide()
        $(".modify-password").hide()
        $(".reset-password").hide()
    } else if (currentURL.includes('modify-password')) {
        $(".login-content").hide()
        $(".register-content").hide()
        $(".modify-password").show()
        $(".reset-password").hide()
    } else if (currentURL.includes('reset-password')) {
        $(".login-content").hide()
        $(".register-content").hide()
        $(".modify-password").hide()
        $(".reset-password").show()
    } else {
        $(".login-content").hide()
        $(".register-content").hide()
        $(".modify-password").hide()
        $(".reset-password").hide()
    }

    if (pathname === "/") {
        $(".container").hide()
        $(".index-info").show()
    } else {
        $(".index-info").hide()
        $(".container").show()
    }

}

$(function () {

    testCurrentURL()
})
// 注册按钮
$(function () {
    const buttons = $("header nav .auth-model a")
    buttons.eq(1).click(function () {
        testCurrentURL()
    })
    buttons.eq(0).click(function () {
        testCurrentURL()

    })
})
var user

function checkLocalCache() {
    let jsd = localStorage.getItem('user');
    user = JSON.parse(jsd);
    if (user) {
        console.log(user.username)
        $("header nav .auth-model").hide()
        $("header .user-info").show()
        $("header .user-info span ").text('Hi, ' + user.username)
        document.cookie = 'token=' + user.token;  // 将令牌设置为 Cookie 值
        console.log(document.cookie)


    } else {
        document.cookie = 'token=""'
    }
}

checkLocalCache()
$(function () {
    // 选取modal
    // $("#static-exit ").eq(2).find("button").eq(2).click(function () {
    //     // 选中userinfo模块
    //     alert(1)
    //     // $(".modal.fade").eq(2).find("button").eq(0).trigger("click");
    //     // const user = $(" header .auth-model")
    //     // $("header nav .user-info").hide();
    //     // user.show()
    //
    // })
    $("#static-exit button").eq(2).click(function () {
        $("#static-exit button").eq(1).trigger("click");
        const user = $("header .auth-model")
        $("header .user-info").hide()
        user.show()
        window.localStorage.clear();  // 清除本地缓存
        document.cookie = 'token=""'

    })
})

