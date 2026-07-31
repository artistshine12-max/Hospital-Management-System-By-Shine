function updateNotificationBadge(){

    fetch("/notifications/count/")

    .then(response => response.json())

    .then(data => {

        const badge = document.getElementById("notificationBadge");

        if(badge){

            badge.innerHTML = data.count;

            if(data.count == 0){

                badge.style.display = "none";

            }else{

                badge.style.display = "flex";

            }

        }

    });

}

setInterval(updateNotificationBadge,10000);