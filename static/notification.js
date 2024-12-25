/*
    poll every 5 seconds for notifications 
    a seprate app will be made for notifications for every user 
    create a global notifications object that stores notification content and id 
    it will display the content and be updated after every poll 
    only the new notifications will be added to the global object
    uplon clicking on any of the notifications it will be marked as read and the global object will be updated to remove the notification
    the backend will also mark the notification as read and stop sending it to the frontend
    
    mark as read sending request to the backend to mark the notification as read and removing the notification from front end as well
*/

let notifications = []

const notificationMenu = document.getElementById('notificationMenu')
const badge = document.getElementById('badge')



fetch('http://127.0.0.1:8000/notification')
.then(response => response.json())
.then(data => {
    console.log(notifications)
    console.log(data)
    // if (data.notifications.length === 0) {
    //     badge.classList.add("d-none")
    //     return
    // }
    for (const item of data.notifications) {
        const { content, id } = item;
        console.log(content, id )

        // Check if the notification with the same id already exists
        if (notifications.some(notification => notification.id == id)) {
            continue;
        }

        notifications.push({ content, id });

        if (notifications.length > 0) {
            badge.classList.remove("d-none")

            badge.innerHTML = notifications.length
        }

        const btn = document.createElement('button');
        btn.classList.add('dropdown-item', 'text-wrap');
        btn.innerHTML = content;
        btn.dataset.id = id;
        btn.addEventListener('click', markAsRead);

        notificationMenu.appendChild(btn);
    }
   
   
})
.catch(error => {
    console.error('Error:', error);
});

setInterval(() => {
    fetch('http://127.0.0.1:8000/notification')
        .then(response => response.json())
        .then(data => {
            console.log(notifications)
            console.log(data)
            // if (data.notifications.length === 0) {
            //     badge.classList.add("d-none")
            //     return
            // }
            for (const item of data.notifications) {
                const { content, id } = item;
                console.log(content, id )

                // Check if the notification with the same id already exists
                if (notifications.some(notification => notification.id == id)) {
                    continue;
                }

                notifications.push({ content, id });

                if (notifications.length > 0) {
                    badge.classList.remove("d-none")
    
                    badge.innerHTML = notifications.length
                }

                const btn = document.createElement('button');
                btn.classList.add('dropdown-item', 'text-wrap');
                btn.innerHTML = content;
                btn.dataset.id = id;
                btn.addEventListener('click', markAsRead);

                notificationMenu.appendChild(btn);
            }
           
           
        })
        .catch(error => {
            console.error('Error:', error);
        });
}, 1000);


function markAsRead(event) {
    const id = Number(event.target.dataset.id)
    console.log("markAsRead",id)
    fetch(`http://127.0.0.1:8000/notification/markAsRead/${id}`)
        .then(response => response.json())
        .then(data => {
            console.log(data)
            event.target.remove()
            for (let i = 0; i < notifications.length; i++) {
                console.log(i,notifications[i].id,id)
                if (notifications[i].id === id) {
                    notifications.splice(i, 1)
                    console.log(notifications,"after markAsRead",id)
                    break
                }
            }
            badge.innerHTML = notifications.length
            if (notifications.length === 0) {
                badge.classList.add("d-none")
            }
        })
        .catch(error => {
            console.error('Error:', error);
        });
      
}






