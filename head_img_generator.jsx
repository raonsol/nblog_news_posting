// options: IPF, MGEN
var TEMPLATE_TYPE = "IPF";

// IPF: 1=특허, 2=상표디자인, 3=저작권, 4=IP분쟁소송, 5=Startup Info.
//MGEN: 1=BLOCKCHAIN, 2=SMART FACTORY, 3=3DMET
var TEMPLATE_NAME=1;

var NEWSPAPER_NAME ="연합뉴스";
var HEADLINE_CONTENT = "SNS 활용 마케팅 서비스 특허출원 급증…5년간 연평균 28%↑";

var DEST_MGEN="C:/Users/MGEN/Desktop/LYJ/11. Blog/Output/";
var DEST_IPF="C:/Users/MGEN/Desktop/LYJ/00. IPF/Output/";
var TARGET_MGEN="C:/Users/MGEN/Desktop/LYJ/11. Blog/Template/";
var TARGET_IPF="C:/Users/MGEN/Desktop/LYJ/00. IPF/new/";

//return date as yy-mm-dd format
Date.prototype.yymmdd=function(){
    var yy=this.getFullYear().toString();
    var mm=(this.getMonth()+1).toString();
    var dd=this.getDate().toString();
    return yy+"-"+(mm[1]?mm:'0'+mm[0])+"-"+(dd[1]?dd:'0'+dd[0]);
}

var tempTarget=getTarget(TEMPLATE_TYPE, TEMPLATE_NAME);
var doc = getTargetFile(tempTarget);

var tempDest=getDest(TEMPLATE_TYPE);
var outPath = getDatePath(tempDest);
var outName = getOutputName();
var outFile = new File(outPath+outName+".png");

var content={};
content.newspaper=NEWSPAPER_NAME;
content.headline=HEADLINE_CONTENT;
content.date=(new Date()).yymmdd();

if(doc) createImage(content);

function createImage(content){
    //select item in layer
    var layer_content=doc.layers.getByName('Content');
    var item_newspaper = layer_content.pageItems.getByName('newspaper');
    var item_date=layer_content.pageItems.getByName('date');
    var item_headline=layer_content.pageItems.getByName('headline');

    //change content
    item_newspaper.contents=content.newspaper;
    item_date.contents=content.date;
    item_headline.contents=content.headline;

    //export options
    var opt=setOption(300, false, false);
    var color=new RGBColor();
    color.white=255;
    var activeAB = doc.artboards[doc.artboards.getActiveArtboardIndex()];
    
    //export
    doc.imageCapture (outFile, activeAB.artboardRect, opt);
    alert("File exported to" + outFile.toString());
}

function getTarget(type, content){
    var targetPath;
    var targetName;
    if(type=="IPF"){
        targetPath=TARGET_IPF;
        switch(content){
            case 1:
            targetName="01_특허";
            break;
            case 2:
            targetName="02_상표디자인";
            break;
            case 3:
            targetName="03_저작권";
            break;
            case 4:
            targetName="04_IP분쟁소송";
            break;
            case 5:
            targetName="05_Startup information";
            break;
            default:
            alert("Content type mismatch");
            return null;
            }
        return targetPath+targetName+".ai/";
        }
    else if(type=="MGEN"){
        targetPath=TARGET_MGEN;
        switch(content){
            case 1:
            targetName="01_BLOCKCHAIN";
            break;
            case 2:
            targetName="02_SMART_FACTORY";
            break;
            case 3:
            targetName="03_3DMET";
            break;
            default:
            alert("Content type mismatch");
            return null;
            }
        return targetPath+targetName+".ai/";
        }
    else{
        alert ("Blog Type mismatch");
        return null;
    }
}

function getDest(type){
    if(type=="IPF") return DEST_IPF;
    else if(type=="MGEN") return DEST_MGEN;
    else{
        alert ("Type mismatch");
        return null;
    }
}

function setOption(ppi, transparency, matte){
    var options=new ImageCaptureOptions();
    options.resolution=ppi;
    options.transparency=transparency;
    options.matte=matte;
    options.antiAliasing=true;
    
    return options;
}

function getTargetFile(target_path){
    var target=new File(target_path);
    var doc = app.open(target);
    app.userInteractionLevel = UserInteractionLevel.DONTDISPLAYALERTS;
    
    if(doc)
        return doc;
    else{
        alert("There is no such file\n");
        return null;
     }
}

function getDatePath(outpath){
    var date=new Date();
    var year=date.getFullYear().toString();
    var month=(date.getMonth()+1).toString();
    month=month[1]?month:'0'+month[0]
    
    return outpath+year+"/"+month+"/";
}

function getOutputName(){
    var date=new Date();
    var month=(date.getMonth()+1).toString();
    month=month[1]?month:'0'+month[0]
    var day=date.getDate().toString();
    day=day[1]?day:'0'+day[0]
    
    return month+day;
 }

