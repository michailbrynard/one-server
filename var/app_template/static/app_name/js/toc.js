window.onload = function () {
    var toc = "";
    var level = 0;

    document.getElementById("contents").innerHTML =
    	document.getElementById("contents").innerHTML.replace(
    		/<h([\d])>([^<]+)<\/h([\d])>/gi,
    		function (str, openLevel, titleText, closeLevel) {
    			if (openLevel != closeLevel) {
    				return str;
    			}

    			if (openLevel > level) {
    				toc += (new Array(openLevel - level + 1)).join("<ul>");
    			} else if (openLevel < level) {
    				toc += (new Array(level - openLevel + 1)).join("</ul>");
    			}

    			level = parseInt(openLevel);

    			var anchor = titleText.replace(/ /g, "_");
    			toc += "<li><a href=\"#" + anchor + "\">" + "<h" + openLevel + ">" + titleText + "</h" + closeLevel + ">"
    				+ "</a></li>";

    			return "<div class=\"anchor\" id=\"" + anchor + "\" ></div><h" + openLevel + ">" + titleText + "</h" + closeLevel + ">";
    		}
    	);

    if (level) {
    	toc += (new Array(level + 1)).join("</ul>");
    }

    document.getElementById("toc").innerHTML += toc;
};