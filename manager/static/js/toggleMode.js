function toggleMode(page, args='') {
    let currMode = getCookie("theme")
    if (currMode === "lightmode")
        currMode = "darkmode"
    else
        currMode = "lightmode"

    if (page === "archive_entry")
        location.href = "/set/" + currMode + "-" + page + "-" + location.href.split("/")[4]
    else
        location.href = "/set/" + currMode + "-" + page
}

function getCookie(cName) {
      const name = cName + "=";
      const cDecoded = decodeURIComponent(document.cookie); //to be careful
      const cArr = cDecoded .split('; ');
      let res;
      cArr.forEach(val => {
          if (val.indexOf(name) === 0) res = val.substring(name.length);
      })
      return res;
}