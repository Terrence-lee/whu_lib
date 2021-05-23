function site_re(site) {
    alter("2");
}

function test_site(site) {
  if (site.value=="工学部"){
     $("[name='seat0']").html("<option>103支点空间</option><option>103空间双屏云桌面区</option><option>一楼中部走廊</option><option>201自科图书区</option><option>205电阅PC区</option><option>205电阅云桌面区</option><option>205电阅笔记本区</option><option>2楼走廊</option><option>301东自科借阅区</option><option>305中自科借阅区</option><option>307室</option><option>401东自科借阅区</option><option>405中期刊阅览区</option><option>407室</option><option>501东外文借阅区</option><option>505中自科借阅区</option>");
  }
  else if (site.value=="医学部"){
     $("[name='seat0']").html("<option>202中文科技A区</option><option>204教学参考区</option><option>302中文科技B区</option><option>305科技期刊区</option><option>402中文文科区</option><option>405电子阅览室</option><option>502外文区</option><option>503培训教室</option><option>506医学人文区</option>");
 }
  else if (site.value=="总馆"){
     $("[name='seat0']").html("<option>A1座位区</option><option>A1手提电脑区</option><option>A1沙发区</option><option>A1电子阅览室</option><option>B1</option><option>B1共享空间板凳(无桌)</option><option>B1第二培训室</option><option>B2自习区(原C1自习区）</option><option>C1(现场选座)</option><option>E1信息共享空间</option><option>E1信息共享空间双屏云桌面区</option><option>E1文献展示区</option><option>A2借阅区</option><option>A2多媒体VR体验区</option><option>A2多媒体双屏电脑区</option><option>A2多媒体苹果电脑区</option><option>A2多媒体视频工作站区</option><option>B2(现场选座)</option><option>C2(现场选座)</option><option>E2 报刊阅览区</option><option>E2大厅</option><option>北门走廊</option><option>A3</option><option>B3(现场选座)</option><option>C3(现场选座)</option><option>E3 学位论文阅览区</option><option>A4</option><option>B4(现场选座)</option><option>C4(现场选座)</option><option>E4 港台文献阅览区</option><option>A5</option><option>E5 地方文献阅览区</option><option>E6 影印文献（古籍/民国）阅览区</option><option>E7当代艺术文献中心</option>");
 }
 else if (site.value=="信息学部"){
     $("[name='seat0']").html("<option>3C创客双屏电脑</option><option>3C创客咖啡区</option><option>3C创客电子阅读</option><option>3C创客空间</option><option>创新学习云桌面</option><option>创新学习沙发区</option><option>创新学习苹果区</option><option>创新学习讨论区</option><option>东自然科学区</option><option>中厅沙发区</option><option>西自然科学区</option><option>东社会科学区</option><option>中厅沙发区</option><option>自主学习区</option><option>西社会科学区</option><option>东图书阅览区</option><option>西图书阅览区</option>");
 }

}