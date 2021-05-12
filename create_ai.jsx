var TEMPLATE_TARGET = "C:/Users/MGEN/Desktop/LYJ/11. Blog/Template/";
var TEMPLATE_NAME = "01_3DMET.ai"
var TEMPLATE_DEST = "C:/Users/MGEN/Desktop/LYJ/11. Blog/Output/";
var NEWSPAPER_NAME ="한국경제";
var HEADLINE_CONTENT = "만도, VR로 라이다센서 고도화";

//return date as yy-mm-dd format
Date.prototype.yymmdd=function(){
    var yy=this.getFullYear().toString();
    var mm=(this.getMonth()+1).toString();
    var dd=this.getDate().toString();
    return yy+"-"+(mm[1]?mm:'0'+mm[0])+"-"+(dd[1]?dd:'0'+dd[0]);
}

var doc = getTargetFile(TEMPLATE_TARGET+TEMPLATE_NAME);
var output_path = getOutputPath(TEMPLATE_DEST);
var output_name = getOutputName();
var output_file = new File(output_path+output_name+".png");
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
    doc.imageCapture (output_file, activeAB.artboardRect, opt);
    alert("File exported to" + output_file.toString());
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

function getOutputPath(outpath){
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

