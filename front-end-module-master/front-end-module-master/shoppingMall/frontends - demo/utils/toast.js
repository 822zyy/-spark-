export function toastError(title){
  wx.showToast({
      title,
      icon: 'error',
      duration: 2000
    })
}

export function toastSuccess(title){
  wx.showToast({
      title,
      icon: 'success',
      duration: 2000
    })
}