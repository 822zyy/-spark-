Page({
  data: {
      navbarList:['标题1','标题2','标题3','标题4'],
      activeBar:"标题1",
      makeup:['子标题1'],
      activeMakeUp:"子标题1",
      product:['子标题2',],
      activeProduct:"子标题2",
  },
  async onShow(){

  },
 
  changeNavBarItem(e){
    this.setData({
      activeBar:e.target.dataset.item
    })
    // this.onReady()
  },
  changeNavBarSonItemMakeUp(e){
    this.setData({
      activeMakeUp:e.target.dataset.item
    })
    var activeMakeUp = this.data.activeMakeUp
    this.setData({
      makeUpList:this.data.productList.filter(item=>item.makeup == activeMakeUp)
    })
  },
  changeNavBarSonItemProduct(e){
    this.setData({
      activeProduct:e.target.dataset.item
    })
    var activeProduct = this.data.activeProduct
    this.setData({
      productHuaZhuangPingList:this.data.productList.filter(item=>item.type == activeProduct)
    })
  },
 
})
