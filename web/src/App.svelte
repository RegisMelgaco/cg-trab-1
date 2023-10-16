<script>
  let coordinates = {
    1: { x: "0", y: "0" },
    2: { x: "1", y: "1" },
    3: { x: "0", y: "1" },
    4: { x: "1", y: "0" },
  };
  let edges = { 1: { p1: 1, p2: 2 }, 2: { p1: 3, p2: 2 }, 3: { p1: 1, p2: 3 } };
  let curves = { 1: { p1: 1, p2: 2, t1: 3, t2: 4, res: 15 } };
  let polies = { 1: [1, 2, 3] };
  let plots = [];
  let antiAlias = false;
  let verticalRes = 100;
  let horizontalRes = 100;

  async function updatePlots() {
    const resp = await fetch("http://localhost:8080/plots");
    const body = await resp.json();

    plots = body.plots.sort().reverse();
  }

  updatePlots();

  function addCoordinate() {
    let k = 1;
    while (coordinates[k] != undefined) {
      k++;
    }

    coordinates[k] = { x: "0", y: "0" };
  }

  function deleteCoordinate(k) {
    delete coordinates[k];

    coordinates = coordinates;
  }

  function addEdge() {
    let k = 1;
    while (edges[k] != undefined) {
      k++;
    }

    edges[k] = { p1: 1, p2: 2 };
  }

  function deleteEdge(k) {
    delete edges[k];

    edges = edges;
  }

  function addCurve() {
    let k = 1;
    while (curves[k] != undefined) {
      k++;
    }

    curves[k] = { p1: 1, p2: 2, t1: 3, t2: 4, res: 15 };
  }

  function deleteCurve(k) {
    delete curves[k];

    curves = curves;
  }

  function addPoly() {
    let k = 1;
    while (polies[k] != undefined) {
      k++;
    }

    polies[k] = [];
  }

  function selectPolyEdges(poly) {
    return function (e) {
      let edges = [];
      Object.values(e.target.options).forEach((opt) => {
        if (opt.selected) {
          edges.push(parseInt(opt.value));
        }
      });

      polies[poly] = edges;
      console.log(polies);
    };
  }

  function deletePoly(k) {
    delete polies[k];

    polies = polies;
  }

  async function createPlot() {
    const cs = Object.entries(coordinates).map(([k, v]) => [
      k,
      { x: parseInt(v.x), y: parseInt(v.y) },
    ]);

    const body = await JSON.stringify({
      resolution: [verticalRes, horizontalRes],
      coordinates: Object.fromEntries(cs),
      polies,
      curves,
      edges,
    });

    await fetch("http://localhost:8080/raster", {
      method: "POST",
      headers: {
        "Content-type": "application/json",
        Accept: "application/json",
      },
      body,
    });

    updatePlots();
  }
</script>

<main class="container-md">
  <h1 class="mt-5">Rasterização de Retas, Poligonos e Curvas</h1>

  <div class="d-flex p-2 overflow-x-auto">
    {#each plots as p}
      <img alt="plot de {p}" src="http://localhost:8080/static/plots/{p}" class="me-4" style="height: 30rem; {antiAlias ? "" : "image-rendering: pixelated"}" />
    {/each}
  </div>

  <form class="mt-5 mb-5">
    <h2>Adicionar elementos</h2>

    <div class="d-flex mt-4">
      <div class="me-4">
        <label for="plot-height" class="form-label">Resolução Vertical</label>
        <input
          bind:value={verticalRes}
          type="number"
          class="form-control"
          id="plot-height"
        />
      </div>
      <div>
        <label for="plot-width" class="form-label">Resolução Horizontal</label>
        <input
          bind:value={horizontalRes}
          type="number"
          class="form-control"
          id="plot-width"
        />
      </div>
      <div class="me-4 form-check form-switch">
        <input bind:value={antiAlias} class="form-check-input" type="checkbox" id="anti-aliasing">
        <label class="form-check-label" for="anti-aliasing">Anti aliasing</label>
      </div>
    </div>

    <h3 class="mt-5">Coordenadas</h3>

    <table class="table table-striped table-hover">
      <thead>
        <tr class="text-center">
          <th scope="col">#</th>
          <th scope="col">X</th>
          <th scope="col">Y</th>
          <th scope="col" />
        </tr>
      </thead>
      <tbody>
        {#each Object.entries(coordinates) as [k, c]}
          <tr class="text-center">
            <th scope="row">{k}</th>
            <td>
              <input type="number" class="form-control text-center" placeholder="Definição" aria-label="Definição" bind:value={c.x} >
            </td>
            <td>
              <input type="number" class="form-control text-center" placeholder="Definição" aria-label="Definição" bind:value={c.y} >
            </td>
            <td
              ><button
                type="button"
                class="btn btn-link"
                on:click={() => deleteCoordinate(k)}>deletar</button
              ></td
            >
          </tr>
        {/each}
      </tbody>
    </table>

    <div class="d-grid gap-2">
      <button on:click={addCoordinate} class="btn btn-primary" type="button"
        >Adicionar</button
      >
    </div>

    <h3 class="mt-5">Arestas</h3>

    <table class="table table-striped table-hover">
      <thead>
        <tr class="text-center">
          <th scope="col">#</th>
          <th scope="col">P1</th>
          <th scope="col">P2</th>
          <th scope="col" />
        </tr>
      </thead>
      <tbody>
        {#each Object.entries(edges) as [k, v]}
          <tr class="text-center">
            <th scope="row">{k}</th>
            <td>
              <select bind:value={v.p1} class="form-select text-end">
                {#each Object.keys(coordinates) as c}
                  <option value={parseInt(c)}>{c}</option>
                {/each}
              </select>
            </td>
            <td>
              <select bind:value={v.p2} class="form-select text-end">
                {#each Object.keys(coordinates) as c}
                  <option value={parseInt(c)}>{c}</option>
                {/each}
              </select>
            </td>
            <td
              ><button
                type="button"
                class="btn btn-link"
                on:click={() => deleteEdge(k)}>deletar</button
              ></td
            >
          </tr>
        {/each}
      </tbody>
    </table>

    <div class="d-grid gap-2 mb-5">
      <button on:click={addEdge} class="btn btn-primary" type="button"
        >Adicionar</button
      >
    </div>


    <h3 class="mt-5">Curvas</h3>

    <table class="table table-striped table-hover">
      <thead>
        <tr class="text-center">
          <th scope="col">#</th>
          <th scope="col">P1</th>
          <th scope="col">P2</th>
          <th scope="col">T1</th>
          <th scope="col">T2</th>
          <th scope="col">Definição</th>
          <th scope="col" />
        </tr>
      </thead>
      <tbody>
        {#each Object.entries(curves) as [k, v]}
          <tr class="text-center">
            <th scope="row">{k}</th>
            <td>
              <select bind:value={v.p1} class="form-select text-end">
                {#each Object.keys(coordinates) as c}
                  <option value={parseInt(c)}>{c}</option>
                {/each}
              </select>
            </td>
            <td>
              <select bind:value={v.p2} class="form-select text-end">
                {#each Object.keys(coordinates) as c}
                  <option value={parseInt(c)}>{c}</option>
                {/each}
              </select>
            </td>
            <td>
              <select bind:value={v.t1} class="form-select text-end">
                {#each Object.keys(coordinates) as c}
                  <option value={parseInt(c)}>{c}</option>
                {/each}
              </select>
            </td>
            <td>
              <select bind:value={v.t2} class="form-select text-end">
                {#each Object.keys(coordinates) as c}
                  <option value={parseInt(c)}>{c}</option>
                {/each}
              </select>
            </td>
            <td>
              <input type="number" class="form-control text-center" placeholder="Definição" aria-label="Definição" bind:value={v.res} >
            </td>
            <td
              ><button
                type="button"
                class="btn btn-link"
                on:click={() => deleteCurve(k)}>deletar</button
              ></td
            >
          </tr>
        {/each}
      </tbody>
    </table>

    <div class="d-grid gap-2 mb-5">
      <button on:click={addCurve} class="btn btn-primary" type="button"
        >Adicionar</button
      >
    </div>


    <h3 class="mt-5">Poligonos</h3>

    <table class="table table-striped table-hover">
      <thead>
        <tr class="text-center">
          <th scope="col">#</th>
          <th scope="col">Arestas</th>
          <th scope="col" />
        </tr>
      </thead>
      <tbody>
        {#each Object.keys(polies) as k}
          <tr class="text-center">
            <th scope="row">{k}</th>
            <td>
              <select
                on:change={selectPolyEdges(k)}
                class="form-select text-center"
                multiple
              >
                {#each Object.keys(edges) as e}
                  <option selected={polies[k].includes(parseInt(e))} value={e}
                    >{e}</option
                  >
                {/each}
              </select>
            </td>
            <td
              ><button
                type="button"
                class="btn btn-link"
                on:click={() => deletePoly(k)}>deletar</button
              ></td
            >
          </tr>
        {/each}
      </tbody>
    </table>

    <div class="d-grid gap-2 mb-5">
      <button on:click={addPoly} class="btn btn-primary" type="button"
        >Adicionar</button
      >
    </div>

    <div class="d-grid gap-2 mt-5">
      <button on:click={createPlot} class="btn btn-lg btn-success" type="button"
        >Criar</button
      >
    </div>
  </form>
</main>

<style>
</style>
