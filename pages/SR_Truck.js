function createTruckDiagram(containerId, N_ang = 33, angleOffset = 0) {
    // Store elements and settings for this instance
    const instance = {
        canvas: null,
        ctx: null,
        slider: null,
        checkboxRest: null,
        checkboxMoving: null,
        checkboxPaths: null,
        _U: 0, // initially in rest frame
        _Beta: 0.8,
        _Gamma: null, // Will be calculated
        _t: 0,
        _T_tot: null, // Will be calculated
        _N_ang: N_ang,
        _ang: [],
        _paths: [], // Initialize _paths after _N_ang
        _showPaths: true,
    };

    // Now initialize _ang with angleOffset and other dependent properties
    instance._Gamma = 1 / Math.sqrt(1 - Math.pow(instance._Beta, 2));
    instance._ang = Array.from({ length: instance._N_ang }, (_, i) => (2 * Math.PI) * i / instance._N_ang + angleOffset);
    instance._paths = Array.from({ length: instance._N_ang }, () => []);

    // --- Create Elements ---
    const container = document.getElementById(containerId);

    instance.canvas = document.createElement('canvas');
    instance.canvas.id = containerId + '_canvas'; // Unique ID for canvas
    container.appendChild(instance.canvas);

    const timeDiv = document.createElement('div');
    const timeLabel = document.createElement('label');
    timeLabel.htmlFor = containerId + '_timeSlider';
    timeLabel.textContent = 'Time:';
    timeDiv.appendChild(timeLabel);

    instance.slider = document.createElement('input');
    instance.slider.type = 'range';
    instance.slider.id = containerId + '_timeSlider';
    instance.slider.min = 0;
    instance.slider.value = 0;
    instance.slider.style.width = '100%';
    timeDiv.appendChild(instance.slider);
    container.appendChild(timeDiv);

    const frameDiv = document.createElement('div');
    frameDiv.style.display = 'flex';
    frameDiv.style.flexDirection = 'row';
    frameDiv.textContent = 'Frame:';

    instance.checkboxRest = document.createElement('input');
    instance.checkboxRest.type = 'checkbox';
    instance.checkboxRest.id = containerId + '_checkboxRest';
    instance.checkboxRest.checked = true;
    let labelRest = document.createElement('label');
    labelRest.htmlFor = containerId + '_checkboxRest';
    labelRest.textContent = ' Rest ';
    labelRest.appendChild(instance.checkboxRest);
    frameDiv.appendChild(labelRest);

    instance.checkboxMoving = document.createElement('input');
    instance.checkboxMoving.type = 'checkbox';
    instance.checkboxMoving.id = containerId + '_checkboxMoving';
    instance.checkboxMoving.checked = false;
    let labelMoving = document.createElement('label');
    labelMoving.htmlFor = containerId + '_checkboxMoving';
    labelMoving.textContent = ' Moving at 0.8c ';
    labelMoving.appendChild(instance.checkboxMoving);
    frameDiv.appendChild(labelMoving);
    container.appendChild(frameDiv);

    const pathsDiv = document.createElement('div');
    instance.checkboxPaths = document.createElement('input');
    instance.checkboxPaths.type = 'checkbox';
    instance.checkboxPaths.id = containerId + '_checkboxPaths';
    instance.checkboxPaths.checked = true;
    let labelPaths = document.createElement('label');
    labelPaths.htmlFor = containerId + '_checkboxPaths';
    labelPaths.textContent = ' Show Paths ';
    labelPaths.appendChild(instance.checkboxPaths);
    pathsDiv.appendChild(labelPaths);
    container.appendChild(pathsDiv);

    instance.ctx = instance.canvas.getContext('2d');

    // --- Setup ---
    function setup() {
        let divWidth = container.offsetWidth;
        instance._T_tot = 2 * divWidth / (2 * instance._Gamma * instance._Beta + 1 / instance._Gamma + 1);
        let padding_truck = instance._T_tot / 10;
        instance.canvas.width = divWidth;
        instance.canvas.height = instance._T_tot + 10 + padding_truck;
        instance.slider.max = instance._T_tot;
    }

    function resetPaths() {
        instance._paths = Array.from({ length: instance._N_ang }, () => []);
    }

    // --- Event Listeners (using instance properties) ---
    instance.checkboxRest.addEventListener('change', () => {
        if (instance.checkboxRest.checked) {
            instance._U = 0;
            instance.checkboxMoving.checked = false;
            resetPaths();
            draw();
        }
    });

    instance.checkboxMoving.addEventListener('change', () => {
        if (instance.checkboxMoving.checked) {
            instance._U = 0.8;
            instance.checkboxRest.checked = false;
            resetPaths();
            draw();
        }
    });

    instance.checkboxPaths.addEventListener('change', () => {
        instance._showPaths = instance.checkboxPaths.checked;
        draw();
    });

    instance.slider.addEventListener('input', () => {
        instance._t = parseFloat(instance.slider.value);
        draw();
    });

    // --- Drawing Functions (using instance properties) ---
    function draw() {
        instance._t = parseFloat(instance.slider.value);
        let V = [0, -instance._U];
        instance._Gamma = 1 / Math.sqrt(1 - Math.pow(instance._U, 2));
        // Calculate R_source based on time and far-left initial position: -20 _T_tot
        let Width_of_div = instance.canvas.width;
        let R_emit_x = - Width_of_div / 2 + instance._T_tot / 2;
        let R_source = [R_emit_x + instance._U * instance._Gamma * instance._t, -0.5 * instance._T_tot / 10];
        let t_PRM = instance._Gamma * instance._t;
        let Rc_PRM = [];
        let C = [];
        // Initial position remains offset from the top for path drawing:
        let R_initial = [R_emit_x, -0.5 * instance._T_tot / 10];

        for (let I_a = 0; I_a < instance._N_ang; I_a++) {
            let C_PRM = [instance._Gamma * (Math.cos(instance._ang[I_a]) - V[1]), Math.sin(instance._ang[I_a])].map(x => x / (instance._Gamma * (1 - V[1] * Math.cos(instance._ang[I_a]))));
            let Cr_PRM = [instance._Gamma * (-Math.cos(instance._ang[I_a]) - V[1]), -Math.sin(instance._ang[I_a])].map(x => x / (instance._Gamma * (1 - V[1] * -Math.cos(instance._ang[I_a]))));
            let T_reflect_PRM = instance._Gamma * (1 - (V[1] * Math.cos(instance._ang[I_a]))) * instance._T_tot / 2;

            if (t_PRM < T_reflect_PRM) {
                Rc_PRM.push(C_PRM.map(x => x * t_PRM));
                C.push(C_PRM);

                // Store path from initial position to current position
                instance._paths[I_a] = [[R_initial[0], R_initial[1]]]; // Start path at initial R_source
                instance._paths[I_a].push([R_initial[0] + Rc_PRM[I_a][0], R_initial[1] + Rc_PRM[I_a][1]]); // End at current Rc_PRM

            } else {
                // First path segment: from initial position to reflection point
                let reflectionPoint = C_PRM.map(x => x * T_reflect_PRM);
                instance._paths[I_a] = [[R_initial[0], R_initial[1]]]; // Start at initial R_source
                instance._paths[I_a].push([R_initial[0] + reflectionPoint[0], R_initial[1] + reflectionPoint[1]]); // To reflection point

                // Second path segment: from reflection point to current position
                let currentPos = C_PRM.map((x, i) => x * T_reflect_PRM + (t_PRM - T_reflect_PRM) * Cr_PRM[i]);
                Rc_PRM.push(currentPos);
                C.push(Cr_PRM);
                instance._paths[I_a].push([R_initial[0] + currentPos[0], R_initial[1] + currentPos[1]]); // End at current position
            }
        }

        instance.ctx.clearRect(0, 0, instance.canvas.width, instance.canvas.height);

        instance.ctx.save();
        instance.ctx.translate(instance.canvas.width / 2, instance.canvas.height / 2);
        instance.ctx.fillStyle = "#fff";
        instance.ctx.strokeStyle = "#000";
        instance.ctx.lineWidth = 2;

        let Rs_x = R_source[0];
        let Rs_y = R_source[1];
        let w = instance._T_tot / instance._Gamma;
        let h = instance._T_tot;

        let offsetX = w / 5;
        let bottomY = Rs_y + h / 2;
        let leftX = Rs_x - (w / 2) + offsetX;
        let rightX = Rs_x + (w / 2) - offsetX;

        instance.ctx.fillStyle = "#000";
        // Centering the ellipses:
        drawEllipse(instance.ctx, leftX - w / 10 / instance._Gamma, bottomY - h / 10, w / 5 / instance._Gamma, h / 5);
        drawEllipse(instance.ctx, rightX - w / 10 / instance._Gamma, bottomY - h / 10, w / 5 / instance._Gamma, h / 5);
        instance.ctx.fillStyle = "#646464";
        instance.ctx.fillRect(Rs_x - w / 2, Rs_y - h / 2, w, h);
        instance.ctx.lineWidth = 2;       // Set border thickness (adjust as needed)
        instance.ctx.strokeRect(Rs_x - w / 2, Rs_y - h / 2, w, h); // Draw stroked rectangle
        instance.ctx.fillStyle = "#fff";
        // Centering the larger ellipse:
        drawEllipse(instance.ctx, Rs_x - w / 2, Rs_y - h / 2, w, h);

        for (let i = 0; i < Rc_PRM.length; i++) {
            let pos = Rc_PRM[i];
            let dir = C[i];
            let C_mag = Math.sqrt(dir[0] * dir[0] + dir[1] * dir[1]);
            dir[0] /= C_mag;
            dir[1] /= C_mag;
            dir[0] *= 20;
            dir[1] *= 20;

            // Draw the path only if _showPaths is true
            if (instance._showPaths) {
                instance.ctx.strokeStyle = "#000";
                instance.ctx.lineWidth = 1.5;
                instance.ctx.setLineDash([7, 2]);
                instance.ctx.beginPath();
                instance.ctx.moveTo(instance._paths[i][0][0], instance._paths[i][0][1]);
                for (let j = 1; j < instance._paths[i].length; j++) {
                    instance.ctx.lineTo(instance._paths[i][j][0], instance._paths[i][j][1]);
                }
                instance.ctx.stroke();
                instance.ctx.setLineDash([]);
            }

            // Draw the arrow at the end of the path
            instance.ctx.save();
            instance.ctx.fillStyle = "#f00";
            instance.ctx.translate(instance._paths[i][instance._paths[i].length - 1][0], instance._paths[i][instance._paths[i].length - 1][1]);
            instance.ctx.rotate(Math.atan2(dir[1], dir[0]));
            let arrowSize = 10;
            instance.ctx.beginPath();
            instance.ctx.moveTo(C_mag - arrowSize / 2, arrowSize / 2);
            instance.ctx.lineTo(C_mag - arrowSize / 2, -arrowSize / 2);
            instance.ctx.lineTo(C_mag - arrowSize / 2 + arrowSize, 0);
            instance.ctx.closePath();
            instance.ctx.fill();
            instance.ctx.restore();
        }

        instance.ctx.save();
        instance.ctx.fillStyle = 'red'; // Changed stroke to fill
        //instance.ctx.lineWidth = 10; // Removed linewidth
        instance.ctx.beginPath();
        //instance.ctx.moveTo(R_source[0], R_source[1]); // Removed moveTo and lineTo
        //instance.ctx.lineTo(R_source[0]+1, R_source[1]+1);
        instance.ctx.arc(R_source[0], R_source[1], 5, 0, 2 * Math.PI); // Added filled circle
        //instance.ctx.stroke(); // Removed stroke
        instance.ctx.fill(); // Added fill
        instance.ctx.restore();

        instance.ctx.restore();
    }

    function drawEllipse(ctx, x, y, w, h) {
        ctx.beginPath();
        ctx.ellipse(x + w / 2, y + h / 2, w / 2, h / 2, 0, 0, 2 * Math.PI);
        ctx.fill();
        ctx.stroke();
    }

    function windowResized() {
        let divWidth = container.offsetWidth;
        instance._Gamma = 1 / Math.sqrt(1 - Math.pow(instance._Beta, 2));
        instance._T_tot = 2 * divWidth / (2 * instance._Gamma * instance._Beta + 1 / instance._Gamma + 1);
        let padding_truck = instance._T_tot / 10;
        instance.canvas.width = divWidth;
        instance.canvas.height = instance._T_tot + 10 + padding_truck;
        instance.slider.max = instance._T_tot;
        resetPaths();
        draw();
    }

    setup();
    draw();
    window.addEventListener('resize', windowResized);

    // --- Return Control Object (Optional) ---
    return {
        setSpeed: (newSpeed) => {
            // Example method to change the speed
            instance._U = newSpeed;
            instance._Gamma = 1 / Math.sqrt(1 - Math.pow(instance._U, 2));
            instance.checkboxRest.checked = instance._U == 0;
            instance.checkboxMoving.checked = instance._U != 0;
            resetPaths();
            draw();
        },
        // You could add more methods here to control other aspects
        // of the diagram if needed.
    };
}