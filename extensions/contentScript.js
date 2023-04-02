function load() {
    console.log('test')
    const link = document.getElementById("link");
    console.log(link)
    console.log(window.location)
    console.log(window.location.href)
    chrome.tabs.query(
        {
            currentWindow: true,    // currently focused window
            active: true            // selected tab
        },
        function (foundTabs) {
            if (foundTabs.length > 0) {
                var url = foundTabs[0].url;
                console.log(url)
                fetch('http://localhost:8000/feed/get-question/', {
                    method: 'POST',
                    headers: {
                        'Accept': 'application/json',
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ "url": url, 'test': 'here' })
                })
                .then(response => response.json())
                .then((data) => {
                    if (data.status == "exists") {
                        link.href = "https://www.youtube.com/watch?v=qp6e0tucEhw&list=PL_c9BZzLwBRKFRIBWEWYCnV4Lk9HE3eYJ/"
                        link.innerHTML = "Watch Video"
                    } else {
                        link.href = data.meet_link
                        link.innerHTML = "Video Chat"
                    }
                  });
                if (url === "https://stackoverflow.com/questions/879432/what-is-the-difference-between-a-generative-and-a-discriminative-algorithm") {
                    link.innerHTML = "Watch Video"
                } else if (url === "https://stackoverflow.com/questions/1832076/what-is-the-difference-between-supervised-learning-and-unsupervised-learning") {
                    link.innerHTML = "https://google.com"
                } else if (url === "https://stackoverflow.com/questions/22876978/loop-inside-react-jsx") {
                    link.innerHTML = "https://amazon.com"
                } else {
                    link.href = "http://localhost:3000/room/561a1d70-69e7-4448-9351-9bf9e44c2509/"
                    link.innerHTML = "Video Chat"

                } // <--- this is what you are looking for
            } else {
                // there's no window or no selected tab
            }
        }
    );
   
}
load();