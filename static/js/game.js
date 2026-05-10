(() => {
    const canvas = document.getElementById("game-canvas");
    const ctx = canvas.getContext("2d");

    const btnStart = document.getElementById("btn-start");
    const btnStep = document.getElementById("btn-step");
    const btnClear = document.getElementById("btn-clear");
    const btnJoin = document.getElementById("btn-join");
    const btnResize = document.getElementById("btn-resize");
    const btnPattern = document.getElementById("btn-pattern");
    const btnSave = document.getElementById("btn-save");
    const fileInput = document.getElementById("file-input");
    const roomInput = document.getElementById("room-input");
    const roomStatus = document.getElementById("room-status");
    const speedSlider = document.getElementById("speed-slider");
    const speedValue = document.getElementById("speed-value");
    const gridWidth = document.getElementById("grid-width");
    const gridWidthValue = document.getElementById("grid-width-value");
    const gridHeight = document.getElementById("grid-height");
    const gridHeightValue = document.getElementById("grid-height-value");
    const patternSelect = document.getElementById("pattern-select");
    const genDisplay = document.getElementById("generation");
    const aliveDisplay = document.getElementById("alive-count");
    const toast = document.getElementById("toast");

    let grid = [];
    let paused = true;
    let ancho = 60;
    let largo = 35;
    let cellSize = 14;
    let currentRoom = "default";
    let generation = 0;

    const COLORS = {
        bg: "#13151d",
        gridLine: "#1e2233",
        cellAlive: "#6366f1",
        cellGlow: "rgba(99, 102, 241, 0.15)",
    };

    // --- Socket.IO ---
    const socket = io();

    socket.on("connect", () => {
        socket.emit("join", { room: currentRoom });
        loadPatterns();
    });

    socket.on("estado", (data) => {
        grid = data.grid;
        paused = data.paused;
        ancho = data.ancho;
        largo = data.largo;
        speedSlider.value = data.velocidad;
        speedValue.textContent = data.velocidad + "ms";
        gridWidth.value = ancho;
        gridWidthValue.textContent = ancho;
        gridHeight.value = largo;
        gridHeightValue.textContent = largo;
        generation = 0;
        updateUI();
        resizeCanvas();
        drawGrid();
    });

    socket.on("update_grid", (data) => {
        grid = data.grid;
        if (data.tablero_vacio) {
            paused = true;
            showToast("El tablero está vacío — simulación pausada");
        }
        if (data.paused !== undefined) paused = data.paused;
        generation++;
        updateUI();
        drawGrid();
    });

    // --- Canvas rendering ---

    function resizeCanvas() {
        const container = document.querySelector(".canvas-container");
        const maxW = container.clientWidth - 20;
        const maxH = container.clientHeight - 20;
        cellSize = Math.max(4, Math.min(Math.floor(maxW / ancho), Math.floor(maxH / largo)));
        canvas.width = cellSize * ancho;
        canvas.height = cellSize * largo;
        drawGrid();
    }

    function drawGrid() {
        ctx.fillStyle = COLORS.bg;
        ctx.fillRect(0, 0, canvas.width, canvas.height);

        ctx.strokeStyle = COLORS.gridLine;
        ctx.lineWidth = 0.5;

        for (let x = 0; x <= ancho; x++) {
            ctx.beginPath();
            ctx.moveTo(x * cellSize, 0);
            ctx.lineTo(x * cellSize, canvas.height);
            ctx.stroke();
        }
        for (let y = 0; y <= largo; y++) {
            ctx.beginPath();
            ctx.moveTo(0, y * cellSize);
            ctx.lineTo(canvas.width, y * cellSize);
            ctx.stroke();
        }

        let aliveCount = 0;
        for (let y = 0; y < largo; y++) {
            for (let x = 0; x < ancho; x++) {
                if (grid[y] && grid[y][x]) {
                    aliveCount++;
                    if (cellSize > 6) {
                        ctx.fillStyle = COLORS.cellGlow;
                        ctx.fillRect(
                            x * cellSize - 1,
                            y * cellSize - 1,
                            cellSize + 2,
                            cellSize + 2
                        );
                    }
                    ctx.fillStyle = COLORS.cellAlive;
                    const pad = cellSize > 8 ? 1 : 0;
                    ctx.beginPath();
                    const r = cellSize > 10 ? 2 : 1;
                    const cx1 = x * cellSize + pad;
                    const cy1 = y * cellSize + pad;
                    const cw = cellSize - pad * 2;
                    const ch = cellSize - pad * 2;
                    if (cellSize > 8) {
                        roundRect(ctx, cx1, cy1, cw, ch, r);
                    } else {
                        ctx.fillRect(cx1, cy1, cw, ch);
                    }
                }
            }
        }
        aliveDisplay.textContent = aliveCount;
        genDisplay.textContent = generation;
    }

    function roundRect(ctx, x, y, w, h, r) {
        ctx.beginPath();
        ctx.moveTo(x + r, y);
        ctx.lineTo(x + w - r, y);
        ctx.quadraticCurveTo(x + w, y, x + w, y + r);
        ctx.lineTo(x + w, y + h - r);
        ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h);
        ctx.lineTo(x + r, y + h);
        ctx.quadraticCurveTo(x, y + h, x, y + h - r);
        ctx.lineTo(x, y + r);
        ctx.quadraticCurveTo(x, y, x + r, y);
        ctx.closePath();
        ctx.fill();
    }

    function updateUI() {
        btnStart.textContent = paused ? "Iniciar" : "Detener";
        btnStart.classList.toggle("active", !paused);
    }

    // --- User interactions ---

    canvas.addEventListener("click", (e) => {
        const rect = canvas.getBoundingClientRect();
        const x = Math.floor((e.clientX - rect.left) / cellSize);
        const y = Math.floor((e.clientY - rect.top) / cellSize);
        if (x >= 0 && x < ancho && y >= 0 && y < largo) {
            socket.emit("toggle_celda", { room: currentRoom, x, y });
        }
    });

    btnStart.addEventListener("click", () => {
        if (paused) {
            socket.emit("start", { room: currentRoom });
        } else {
            socket.emit("stop", { room: currentRoom });
        }
    });

    btnStep.addEventListener("click", () => {
        fetch("/api/avanzar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ room: currentRoom }),
        })
            .then((r) => r.json())
            .then((data) => {
                grid = data.grid;
                paused = data.paused;
                if (data.tablero_vacio) showToast("El tablero está vacío");
                generation++;
                updateUI();
                drawGrid();
            });
    });

    btnClear.addEventListener("click", () => {
        socket.emit("borrar", { room: currentRoom });
        generation = 0;
    });

    btnJoin.addEventListener("click", () => {
        const newRoom = roomInput.value.trim();
        if (!newRoom) return;
        socket.emit("leave", { room: currentRoom });
        currentRoom = newRoom;
        roomStatus.textContent = "Sala: " + currentRoom;
        generation = 0;
        socket.emit("join", { room: currentRoom });
    });

    speedSlider.addEventListener("input", () => {
        speedValue.textContent = speedSlider.value + "ms";
        socket.emit("speed", { room: currentRoom, velocidad: parseInt(speedSlider.value) });
    });

    gridWidth.addEventListener("input", () => {
        gridWidthValue.textContent = gridWidth.value;
    });

    gridHeight.addEventListener("input", () => {
        gridHeightValue.textContent = gridHeight.value;
    });

    function hayceldasVivas() {
        for (let y = 0; y < largo; y++) {
            for (let x = 0; x < ancho; x++) {
                if (grid[y] && grid[y][x]) return true;
            }
        }
        return false;
    }

    btnResize.addEventListener("click", () => {
        const w = parseInt(gridWidth.value);
        const h = parseInt(gridHeight.value);
        if (w >= 10 && w <= 150 && h >= 10 && h <= 80) {
            if (hayceldasVivas() && !confirm("El tablero tiene celdas vivas. ¿Desea redimensionar? Se perderán los datos.")) return;
            socket.emit("redimensionar", { room: currentRoom, ancho: w, largo: h });
            generation = 0;
        }
    });

    btnPattern.addEventListener("click", () => {
        const id = patternSelect.value;
        if (!id) return;
        if (hayceldasVivas() && !confirm("El tablero tiene celdas vivas. ¿Desea colocar el patrón? Se perderán los datos.")) return;
        socket.emit("patron", { room: currentRoom, patron_id: id });
        generation = 0;
    });

    btnSave.addEventListener("click", () => {
        fetch("/api/guardar", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ room: currentRoom }),
        })
            .then((r) => {
                if (!r.ok) return r.json().then((d) => { throw new Error(d.error); });
                return r.blob();
            })
            .then((blob) => {
                const url = URL.createObjectURL(blob);
                const a = document.createElement("a");
                a.href = url;
                a.download = "juego_de_la_vida.json";
                a.click();
                URL.revokeObjectURL(url);
                showToast("Archivo guardado");
            })
            .catch((err) => showToast(err.message));
    });

    fileInput.addEventListener("change", () => {
        const file = fileInput.files[0];
        if (!file) return;

        if (!file.name.toLowerCase().endsWith(".json")) {
            showToast("Solo se permiten archivos .json");
            fileInput.value = "";
            return;
        }

        if (file.size > 1024 * 1024) {
            showToast("El archivo es demasiado grande (máximo 1 MB)");
            fileInput.value = "";
            return;
        }

        if (hayceldasVivas() && !confirm("El tablero tiene celdas vivas. ¿Desea cargar un archivo? Se perderán los datos.")) {
            fileInput.value = "";
            return;
        }

        const form = new FormData();
        form.append("file", file);
        form.append("room", currentRoom);
        fetch("/api/cargar", { method: "POST", body: form })
            .then((r) => r.json().then((data) => ({ ok: r.ok, data })))
            .then(({ ok, data }) => {
                if (!ok || data.error) {
                    showToast(data.error || "Error al cargar el archivo");
                    return;
                }
                grid = data.grid;
                paused = data.paused;
                ancho = data.ancho;
                largo = data.largo;
                gridWidth.value = ancho;
                gridWidthValue.textContent = ancho;
                gridHeight.value = largo;
                gridHeightValue.textContent = largo;
                generation = 0;
                updateUI();
                resizeCanvas();
                drawGrid();
                showToast("Archivo cargado");
            })
            .catch(() => showToast("Error al procesar el archivo"));
        fileInput.value = "";
    });

    // --- Helpers ---

    function loadPatterns() {
        fetch("/api/patrones")
            .then((r) => r.json())
            .then((patterns) => {
                patterns.forEach((p) => {
                    const opt = document.createElement("option");
                    opt.value = p.id;
                    opt.textContent = p.nombre;
                    patternSelect.appendChild(opt);
                });
            });
    }

    let toastTimeout;
    function showToast(msg) {
        toast.textContent = msg;
        toast.classList.remove("hidden");
        clearTimeout(toastTimeout);
        toastTimeout = setTimeout(() => toast.classList.add("hidden"), 3000);
    }

    window.addEventListener("resize", resizeCanvas);
    resizeCanvas();
})();
