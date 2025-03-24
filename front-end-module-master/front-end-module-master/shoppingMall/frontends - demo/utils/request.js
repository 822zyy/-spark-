import {toastError,toastSuccess} from './toast'
const delay = () =>{
    return new Promise((resolve)=>{
        setTimeout(()=>{
            resolve()
        },500)
    })
}
const loading = async ()=>{
    wx.showLoading({
        title: '加载中...',
    })
    await delay();
}
const hideLoading = ()=>{
    wx.hideLoading()
}

export default function (url, data='', method="GET") { //封装http请求
  const apiUrl = 'http://localhost:8000' //请求域名
  return new Promise(async (resolve, reject) => {
    await loading()
    wx.request({
      url: apiUrl + url,
      data,
      method: method,
      header:{
        'content-type':"application/x-www-form-urlencoded",
      },
      success: function (res) {
        if(res.data.code != 200){
          hideLoading()
          toastError(res.data.message)
          resolve("")
        }else{
          hideLoading()
          toastSuccess(res.data.message)
          resolve(res.data)
        }
      },
      fail: function (res) {
        reject(res);
      },
      complete: function () {
        console.log('complete');
      }
    })
  })
}