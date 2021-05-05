function doClick() {
       if(String(document.location.href).includes("/dataingest/upload")){
         document.location.href = "../../datasheet-documentation";
       } else if(String(document.location.href).includes("/crud/model-set")){
         document.location.href = "../../datasheet-documentation#select4";
       } else if(String(document.location.href).includes("#collection-body")){
         document.location.href = "../studentData-documentation";
       } else if(String(document.location.href).includes("/crud/students")){
         document.location.href = "../../database-documentation#select1";
       } else if(String(document.location.href).includes("/crud/teachers")){
         document.location.href = "../../database-documentation#select2";
       } else if(String(document.location.href).includes("/crud/schedules")){
         document.location.href = "../../database-documentation#select3";
       } else if(String(document.location.href).includes("/crud/courses")){
         document.location.href = "../../database-documentation#select4";
       } else if(String(document.location.href).includes("/crud/sections")){
         document.location.href = "../../database-documentation#select5";
       } else if(String(document.location.href).includes("/crud/create-bulk-sections")){
         document.location.href = "../../databaseUp-documentation#select8";
       }else if(String(document.location.href).includes("/crud/create-preference")){
         document.location.href = "../../database-documentation#select6";
       } else if(String(document.location.href).includes("/crud/preferences")){
         document.location.href = "../../database-documentation#select6";
       } else if(String(document.location.href).includes("/set-crud/courses")){
         document.location.href = "../../databaseUp-documentation#select7";
       } else if(String(document.location.href).includes("/set-crud/students")){
         document.location.href = "../../databaseUp-documentation";
       } else if(String(document.location.href).includes("/set-crud/preferences")){
         document.location.href = "../../databaseUp-documentation#select9";
       } else if(String(document.location.href).includes("/check-schedule")){
         document.location.href = "schedule-documentation#select1";
       } else if(String(document.location.href).match(/.*schedule\/.*\/.*/)){
         document.location.href = "../../schedule-documentation#select2";
       }
       else {
         document.location.href = "";
         document.location.href = "/docs";
       }
}