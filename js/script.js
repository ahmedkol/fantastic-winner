var menuam = document.getElementById("menu").getElementsByTagName("li");
var headline = document.getElementById("text");
var mydom = document.getElementById("menu");
var btn = document.getElementById("zar");
var counter = 1;
//for (i = 0; i < menuam.length; i++){
   // menuam[i].addEventListener("click", selectItem);
 //}
 

mydom.addEventListener("click", selectItem)

 function selectItem(n){
    if (n.target.nodeName == "LI")

        headline.innerHTML = n.target.innerHTML;
        for (i = 0; i < menuam.length; i++){
          menuam[i].classList.remove("selected");
        }
        n.target.classList.add("selected");

 };
 
 

 btn.addEventListener("click", newItem);


 function newItem(){
    headline.innerHTML = "هم مجرد مبتدئين يتسعملون الادوات ولا يعلمون طريقة عملها"
    btn.innerHTML = "اعد تحميل الصفحه للعوده"
    menuam[0].innerHTML = "Done"
    menuam[1].innerHTML = "Done"
    menuam[2].innerHTML = "Done"
    mydom.innerHTML += "<li> " + counter +"-script Kiddies:مصطلح نصف به المبتدئين الذين يقومون بي تنفيذ الأوامر من غير فهم و معرفه </li>"
    mydom.innerHTML += "<li> " + counter +"-لقبعة الحمراء :م مرة أخرى مزيج من قراصنة القبعة السوداء والقبعات البيضاء. عادة ما تكون على مستوى اختراق الوكالات الحكومية ومراكز المعلومات السرية للغاية وأي شيء يندرج بشكل عام ضمن فئة المعلومات"
    counter++;
 }


   

   