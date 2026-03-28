
<div id="chat">
    <div id="chat-messages">
        <div id="chat-header">
            <div class="row">
                <div class="smaller-image">
                    % include('components/svg', name='ai')
                </div>
                % include('components/svg', name='bctracker/bctracker')
                <div class="smaller-image mirrored">
                    % include('components/svg', name='ai')
                </div>
            </div>
            <h2>Introducing Giuseppe, the BCTracker AI Chat</h2>
            <p class="smaller-font lighter-text">Responses are guaranteed to be 100% accurate</p>
            <hr />
        </div>
        <div id="chat-placeholder">
            <p>Not sure what to ask? Try these unique and carefully tailored prompts:</p>
            <div class="button" onclick="send('When is the next bus leaving?')">When is the next bus leaving?</div>
            <div class="button" onclick="send('Where am I?')">Where am I?</div>
            <div class="button" onclick="send('How did I get here?')">How did I get here?</div>
        </div>
        <div id="chat-thinking" style="display: none;">
            <div class="loader"></div>
            Thinking...
        </div>
    </div>
    <div id="chat-input-container">
        <form onsubmit="sendFromInput()" action="javascript:void(0)">
            <input type="text" id="chat-input" name="chat-input" method="post" size="20" placeholder="Ask any question...">
        </form>
    </div>
</div>

<script>
    const messages = [];
    let thinking = false;
    
    const chatMessagesElement = document.getElementById("chat-messages");
    const chatPlaceholderElement = document.getElementById("chat-placeholder");
    const chatThinkingElement = document.getElementById("chat-thinking");
    
    class Message {
        constructor(actor, response) {
            this.actor = actor;
            this.text = response.message;
            this.data = response.data;
            
            const element = document.createElement("div");
            element.classList.add("message", actor);
            this.element = element;
        }
        
        show() {
            chatMessagesElement.appendChild(this.element);
            if (this.actor === "bot") {
                let index = 1;
                const message = this;
                this.interval = setInterval(function () {
                    if (index >= message.text.length) {
                        message.element.innerHTML = message.text;
                        clearInterval(message.interval);
                        thinking = false;
                        updateThinking();
                        message.showData();
                    } else {
                        message.element.innerHTML = message.text.substring(0, index);
                        index += 1;
                    }
                    chatMessagesElement.scrollTo(0, chatMessagesElement.scrollHeight);
                }, 20);
            } else {
                this.element.innerHTML = this.text;
            }
        }
        
        showData() {
            if (this.data === null || this.data === undefined) {
                return;
            }
            
            const headerElement = this.getHeaderElement(this.data.type);
            this.element.appendChild(headerElement);
            
            if (this.data.type === "route") {
                const dataElement = this.getRouteDataElement(this.data.route);
                this.element.appendChild(dataElement);
            } else if (this.data.type === "route_list") {
                for (const route of this.data.routes) {
                    const dataElement = this.getRouteDataElement(route);
                    this.element.appendChild(dataElement);
                }
            } else if (this.data.type === "stop") {
                const dataElement = this.getStopDataElement(this.data.stop);
                this.element.appendChild(dataElement);
            } else if (this.data.type === "stop_list") {
                for (const stop of this.data.stops) {
                    const dataElement = this.getStopDataElement(stop);
                    this.element.appendChild(dataElement);
                }
            } else if (this.data.type === "vehicle") {
                const dataElement = this.getVehicleDataElement(this.data.vehicle);
                this.element.appendChild(dataElement);
            }
        }
        
        getHeaderElement(type) {
            const headerElement = document.createElement("div");
            headerElement.classList.add("message-data-header");
            
            const iconElement = document.createElement("div");
            const nameElement = document.createElement("div");
            if (type === "route") {
                iconElement.innerHTML = getSVG("route");
                nameElement.innerHTML = "Route";
            } else if (type === "route_list") {
                iconElement.innerHTML = getSVG("route");
                nameElement.innerHTML = "Routes";
            } else if (type === "stop") {
                iconElement.innerHTML = getSVG("stop");
                nameElement.innerHTML = "Stop";
            } else if (type === "stop_list") {
                iconElement.innerHTML = getSVG("stop");
                nameElement.innerHTML = "Stops";
            } else if (type === "vehicle") {
                iconElement.innerHTML = getSVG("bus");
                nameElement.innerHTML = "Bus";
            }
            headerElement.appendChild(iconElement);
            headerElement.appendChild(nameElement);
            
            return headerElement;
        }
        
        getRouteDataElement(route) {
            const numberElement = document.createElement("span");
            numberElement.classList.add("route");
            numberElement.style.backgroundColor = "#" + route.colour;
            numberElement.innerHTML = route.number;
            
            const linkElement = document.createElement("a");
            linkElement.href = getUrl(route.system_id, "routes/" + route.url_id, true);
            linkElement.innerHTML = route.name;
            
            const infoElement = document.createElement("div");
            infoElement.classList.add("column");
            infoElement.appendChild(linkElement);
            infoElement.innerHTML += "<span class='smaller-font lighter-text'>" + route.system_name + "</span>";
            
            const dataElement = document.createElement("div");
            dataElement.classList.add("message-data", "row");
            dataElement.appendChild(numberElement);
            dataElement.appendChild(infoElement);
            
            return dataElement;
        }
        
        getStopDataElement(stop) {
            const stopElement = document.createElement("div");
            stopElement.classList.add("stop");
            stopElement.innerHTML = "<a class='stop-name' href='" + getUrl(stop.system_id, "stops/" + stop.url_id) + "'>" + stop.name + "</a>";
            if (stop.number) {
                stopElement.innerHTML += "<div class='stop-number'>" + stop.number + "</div>";
            }
            
            const routesElement = document.createElement("div");
            routesElement.className = "route-list";
            for (const route of stop.routes) {
                routesElement.innerHTML += "<span class='route' style='background-color: #" + route.colour + ";'>" + route.number + "</span>";
            }
            
            const dataElement = document.createElement("div");
            dataElement.classList.add("message-data", "column");
            dataElement.appendChild(stopElement);
            dataElement.innerHTML += "<span class='smaller-font lighter-text'>" + stop.system_name + "</span>";
            dataElement.appendChild(routesElement);
            
            return dataElement;
        }
        
        getVehicleDataElement(vehicle) {
            const iconElement = document.createElement("div");
            iconElement.innerHTML = getSVG(vehicle.icon);
            
            const vehicleElement = document.createElement("div");
            vehicleElement.innerHTML = "<a href='" + getUrl(currentSystemID, "bus/" + vehicle.url_id) + "'>" + vehicle.name + "</a>";
            if (vehicle.decoration != null) {
                vehicleElement.innerHTML += " <span class='decoration'>" + vehicle.decoration + "</span>";
            }
            
            const infoElement = document.createElement("div");
            infoElement.classList.add("column");
            infoElement.appendChild(vehicleElement);
            infoElement.innerHTML += "<span class='smaller-font lighter-text'>" + vehicle.year_model + "</span>";
            
            const dataElement = document.createElement("div");
            dataElement.classList.add("message-data", "row");
            dataElement.appendChild(iconElement);
            dataElement.appendChild(infoElement);
            
            return dataElement;
        }
    }
    
    function sendFromInput() {
        if (thinking) {
            return;
        }
        const inputElement = document.getElementById("chat-input");
        const text = inputElement.value;
        inputElement.value = "";
        send(text);
    }
    
    function send(text) {
        thinking = true;
        const message = new Message("user", { 'message': text });
        messages.push(message);
        message.show();
        
        updatePlaceholder();
        updateThinking();
        chatMessagesElement.appendChild(chatThinkingElement);
        chatMessagesElement.scrollTo(0, chatMessagesElement.scrollHeight);
        
        setTimeout(function () {
            const request = new XMLHttpRequest();
            request.open("POST", "{{ get_url(context, 'api', 'chat') }}", true);
            request.responseType = "json";
            request.onload = function() {
                if (request.status === 200) {
                    const response = new Message("bot", request.response);
                    messages.push(response);
                    response.show();
                    chatMessagesElement.appendChild(chatThinkingElement);
                } else {
                    const response = new Message("error", "Invalid status code: " + request.status);
                    messages.push(response);
                    response.show();
                    thinking = false;
                    updateThinking();
                }
            };
            request.onerror = function(error) {
                const response = new Message("error", error);
                messages.push(response);
                response.show();
                chatMessagesElement.appendChild(chatThinkingElement);
            };
            const data = new FormData();
            data.set("text", text);
            request.send(data);
        }, 2000);
    }
    
    function updatePlaceholder() {
        if (messages.length === 0) {
            chatPlaceholderElement.style.display = "flex";
        } else {
            chatPlaceholderElement.style.display = "none";
        }
    }
    
    function updateThinking() {
        if (thinking) {
            chatThinkingElement.style.display = "flex";
        } else {
            chatThinkingElement.style.display = "none";
        }
    }
</script>

<style>
</style>
