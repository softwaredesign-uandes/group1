$(document).ready(function() {

    if (WEBGL.isWebGLAvailable() === false) {
        document.body.appendChild( WEBGL.getWebGLErrorMessage() );
    }

    var camera, scene, renderer;
    var controls;
    var cubeGeometry;
    var blockMeshes = [];
    var dataMap;
    var blocks;
    var blockSize = 50;
    var currentGrade = "Au";
    var transparent = false;
    var blockModelId;
    var mineralDepositId;
    var mineralColors = {
        "Cu": 168,
        "Au": 50
    }

    function fetchMineralDeposits() {
        var url = encodeURI("http://127.0.0.1:8000/mineral_deposits/");	
        fetch(url)
            .then(function(response) {
                var data = response.json();
                var promise = Promise.resolve(data);
                promise.then(function(value) {
                    mineralDeposits = value.mineral_deposits
                    var mineralDepositSelect = $("select#mineral-deposit-select");
                    mineralDeposits.forEach(function(mineralDeposit) {
                        mineralDepositSelect.append($("<option />").val(mineralDeposit.id).text(mineralDeposit.name));
                    })
                });
            });
    }

    function fetchMineralDepositBlocks() {
        var url = encodeURI("http://127.0.0.1:8000/mineral_deposits/" + mineralDepositId + "/");	
        fetch(url)
            .then(function(response) {
                var data = response.json();
                var promise = Promise.resolve(data);
                promise.then(function(value) {
                    blockModels = value.mineral_deposit.block_models
                    var blockModelSelect = $("select#block-model-select");
                    blockModelSelect.find('option').not('#default').remove();
                    if (blockModels.length === 0) {
                        blockModelSelect.attr("disabled", true);
                        blockModelSelect.find('option#default').attr("disabled", false);
                        alert("This Mineral Deposit has no Block Models!");
                    } else {
                        blockModelSelect.attr("disabled", false);
                        blockModels.forEach(function(blockModel) {
                            blockModelSelect.append($("<option />").val(blockModel.id).text(blockModel.name));
                        })
                    }
                });
            });
    }

    $("select#mineral-deposit-select").on("change", function(){
        $("select#mineral-deposit-select option#default").attr("disabled", true);
        mineralDepositId = $("select#mineral-deposit-select option:selected").val();
        fetchMineralDepositBlocks();
    })

    $("select#block-model-select").on("change", function(){
        $("select#block-model-select option#default").attr("disabled", true);
        blockModelId = $("select#block-model-select option:selected").val();
        createObjects();
    })

    $("select#mineral-select").on("change", function(){
        $("select#mineral-select option#default").attr("disabled", true);
        currentGrade = $("select#mineral-select option:selected").val();
        loadBlockModel();
    })

    $("#transparent-toggle").on("change", function(){
        transparent = !transparent;
        loadBlockModel();
    })

    fetchMineralDeposits();
    init();
    animate();

    function init() {
        createScene();
        createLights();
        createCamera();
        createRenderer();
        createCameraControls();
        setEventListeners();
    }
    
    function createScene() {
        scene = new THREE.Scene();
        scene.background = new THREE.Color( 0xf0f0f0 );
    }
    
    function createLights() {
        var ambientLight = new THREE.AmbientLight( 0x606060 );
        scene.add( ambientLight );
    
        var light = new THREE.PointLight( 0xffffff );
        light.position.set( 1000, 1000, 1000 );
        scene.add( light );
    }
    
    function createObjects() {
        function fetchDataMap() {
            var url = encodeURI("http://127.0.0.1:8000/block_models/"+blockModelId+"/data_map");	
            fetch(url)
                .then(function(response) {
                    var data = response.json();
                    var promise = Promise.resolve(data);
                    promise.then(function(value) {
                        dataMap = value.data_map
                        populateMineralSelect();
                        fetchBlocks(blockModelId);
                    });
                });
        }

        function populateMineralSelect() {
            var mineralSelect = $("select#mineral-select");
            mineralSelect.find('option').not('#default').remove();
            if (Object.keys(dataMap.grade).length === 0) {
                mineralSelect.attr("disabled", true);
                mineralSelect.find('option#default').attr("disabled", false);
                alert("This Mineral Deposit has no Minerals!");
            } else {
                mineralSelect.attr("disabled", false);
                for (const [key, value] of Object.entries(dataMap.grade)) {
                    mineralSelect.append($("<option />").text(key));
                }
            }
        }
    
        function fetchBlocks() {
            var url = encodeURI("http://127.0.0.1:8000/block_models/"+blockModelId+"/blocks/");	
            fetch(url)
                .then(function(response) {
                    var data = response.json();
                    var promise = Promise.resolve(data);
                    promise.then(function(value) {
                        blocks = value.blocks
                        loadBlockModel();
                    });
                });
        }
    
        cubeGeometry = new THREE.BoxBufferGeometry( blockSize, blockSize, blockSize );
        fetchDataMap(blockModelId);
    }
    
    function loadBlockModel() {
        var gradeHeader = dataMap.grade[currentGrade];
        var xIndex = dataMap["x"];
        var yIndex = dataMap["y"];
        var zIndex = dataMap["z"];
        function addBlock(block) {
            var cubeMaterial = new THREE.MeshLambertMaterial({
                color: getBlockColor(block), 
                opacity: Math.max(0.01, block[gradeHeader]),
                transparent: transparent 
            });
            var blockMesh = new THREE.Mesh(cubeGeometry, cubeMaterial);
            
            var blockSizeWithOffset = blockSize * 1.1;
            blockMesh.position.set(
                blockSizeWithOffset * block[xIndex],
                blockSizeWithOffset * block[yIndex],
                 blockSizeWithOffset * block[zIndex]
            );
            blockMeshes.push(blockMesh);
            scene.add( blockMesh );        
        }
    
        function getBlockColor(block) {
            if (block[gradeHeader] < 0.001)
                return new THREE.Color(0x999999);
            var hue = mineralColors[currentGrade];
            var lightning = Math.floor(block[gradeHeader] * 70);
            var hsl = "hsl("+ hue + ", 100%, " + lightning + "%)";
            return new THREE.Color(hsl);
        }
    
        clearScene();
        for(var i=0; i<blocks.length; i++) {
            addBlock(blocks[i]);
        }
    }
    
    function createCamera() {
        camera = new THREE.PerspectiveCamera( 45, window.innerWidth / window.innerHeight, 1, 10000 );
        camera.position.set( 2000, 2000, 3300 );
        camera.lookAt( 0, 0, 0 );
        camera.up.set(0, 0, 1);
        scene.add(camera);
    }
    
    function createRenderer() {
        renderer = new THREE.WebGLRenderer( { antialias: true } );
        renderer.setPixelRatio( window.devicePixelRatio );
        renderer.setSize( window.innerWidth, window.innerHeight );
        document.body.appendChild( renderer.domElement );
    }
    
    function createCameraControls() {
        controls = new THREE.OrbitControls( camera, renderer.domElement );
        controls.update();
    }
    
    function setEventListeners() {
        window.addEventListener( 'resize', onWindowResize, false );
    }
    
    function clearScene() {
        for(var i=0; i<blockMeshes.length; i++) {
            scene.remove(blockMeshes[i]);
        }; 
    }
    
    function onWindowResize() {

        camera.aspect = window.innerWidth / window.innerHeight;
        camera.updateProjectionMatrix();
        renderer.setSize( window.innerWidth, window.innerHeight );
    
    }
    
    function animate() {
        requestAnimationFrame( animate );
        controls.update();
        renderer.render( scene, camera );
    }
})