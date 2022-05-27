<template>
  <div class="container mx-auto">
    <h1
      class="text-6xl font-bold flex flex-col place-items-center content-center items-center justify-center mb-16"
    >
      Data Visualizer
    </h1>

    <div
      class="flex place-content-center justify-center items-center gap-x-2 w-1/2 m-auto"
    >
      <div class="w-11/12">
        <label for="data">Dataset</label>
        <textarea
          class="border-2 p-4 outline-none border-gray-400 rounded block w-full"
          id="data"
          type="text"
          v-model="textData[visibleSet]"
        />
      </div>

      <div class="w-2/12">
        <div class="flex gap-x-4">
          <span
            class="cursor-pointer"
            :class="{ 'text-blue-600': visibleSet === 'x' }"
            @click="visibleSet = 'x'"
            >x</span
          >
          <span
            class="cursor-pointer"
            :class="{ 'text-blue-600': visibleSet === 'y' }"
            @click="visibleSet = 'y'"
            >y</span
          >
          <span
            class="cursor-pointer"
            :class="{ 'text-blue-600': visibleSet === 'common' }"
            @click="visibleSet = 'common'"
            >common</span
          >
        </div>
        <label for="separator">Separator</label>
        <input
          class="w-1/2 border-2 text-center outline-none border-gray-400 rounded text-2xl"
          id="separator"
          type="text"
          v-model="separator"
        />
      </div>
    </div>
    <p class="mt-4">{{ data }}</p>
    <div class="flex justify-between">
      <div class="space-x-4">
        <select
          class="bg-transparent border-gray-300 outline-none"
          name=""
          id=""
          v-model="plotType"
        >
          <option disabled value="">Plot Type</option>
          <option :value="type.value" v-for="(type, i) in plotTypes" :key="i">
            {{ type.title }}
          </option>
        </select>
        <select
          class="bg-transparent border-gray-300 outline-none"
          name=""
          id=""
          v-model="kind"
        >
          <option disabled value="">Kind</option>
          <option
            :value="kind.value"
            v-for="(kind, i) in kinds[plotType]"
            :key="i"
          >
            {{ kind.title }}
          </option>
        </select>
      </div>

      <div>
        <div class="flex gap-x-2">
          <span class="font-bold"> sample data </span>
          <select
            class="bg-transparent border-gray-300 outline-none uppercase"
            name=""
            id=""
            v-model="sampleDatasetName"
          >
            <option :value="sampleDatasetNames">
              {{ sampleDatasetNames[0] }}
            </option>
            <option
              v-for="(name, i) in sampleDatasetNames.slice(1)"
              :value="name"
              :key="i"
            >
              {{ name }}
            </option>
          </select>
        </div>

        <div class="flex gap-x-2">
          <button class="font-bold" @click="generateRandomDataSet">
            random data
          </button>
          <input
            class="w-24 border-2 outline-none border-gray-400 rounded"
            type="number"
            placeholder="data length"
            v-model="randomDataLength"
          />
        </div>
      </div>
    </div>
    <button
      class="font-bold text-2xl"
      @click="visualize"
      :disabled="plotType === ''"
    >
      Visualize
    </button>

    <img class="m-auto" :src="img" alt="" />
  </div>
</template>

<script>
export default {
  data() {
    return {
      textData: {
        x: "",
        y: "",
        common: "",
      },
      separator: ",",
      api: "http://localhost:8000",
      img: null,
      plotType: "",
      kind: "",
      visibleSet: "common",
      randomDataLength: 10,
      sampleDatasetName: "",
      sampleDatasetNames: [],
      kinds: {
        relplot: [
          { title: "Scatter", value: "scatter" },
          { title: "Line", value: "line" },
        ],
        displot: [
          { title: "Histogram", value: "hist" },
          { title: "KDE", value: "kde" },
          { title: "ECDF", value: "ecdf" },
        ],
        catplot: [
          { title: "Strip", value: "strip" },
          { title: "Swarm", value: "swarm" },
          { title: "Box", value: "box" },
          { title: "Violin", value: "violin" },
          { title: "Boxen", value: "boxen" },
          { title: "Point", value: "point" },
          { title: "Bar", value: "bar" },
          { title: "Count", value: "count" },
        ],
      },
      plotTypes: [
        { title: "Relational", value: "relplot" },
        { title: "Distribution", value: "displot" },
        { title: "Categorical", value: "catplot" },
      ],
    };
  },
  methods: {
    parseTextData(data) {
      return data.split(this.separator);
    },

    fetchData(api, endpoint, { options, data }) {
      return fetch(
        `${api}${endpoint + "?params=" + JSON.stringify({ options, data })}`
      );
    },

    generateRandomDataSet() {
      this.textData[this.visibleSet] = Array.from(
        { length: this.randomDataLength },
        () => Math.floor(Math.random() * 999)
      ).join(this.separator);
    },

    async getSampleDataNames() {
      return fetch(`${this.api}/sampleDatasetNames`);
    },
    async getSampleDataset(name) {
      return fetch(`${this.api}/sampleDataset/${name}`);
    },

    async visualize() {
      const res = await this.fetchData(this.api, "/graph/", {
        options: {
          plotType: this.plotType,
          args: {
            kind: this.kind,
            /* TODO get other args */
          },
        },
        data: JSON.stringify(this.data),
      });
      const blob = await res.blob();
      this.img = URL.createObjectURL(blob);
    },

    async visualize2() {
      const res = await this.fetchData(this.api, "/graph/", {
        options: {
          plotType: this.plotType,
          args: {
            kind: this.kind,
          },
        },
        data: JSON.stringify(this.data),
      });

      const text = await res.text();
      const parser = new DOMParser();
      this.fig = parser.parseFromString(text, "text/html");

      this.fig = this.fig.getElementsByTagName("svg")[0];
    },
  },
  computed: {
    data() {
      let data = {};
      if (this.textData.x !== "") {
        data.x = this.parseTextData(this.textData.x).map((i) => Number(i));
      }

      if (this.textData.y !== "")
        data.y = this.parseTextData(this.textData.y).map((i) => Number(i));

      if (this.textData.x === "" && this.textData.y === "")
        data = this.parseTextData(this.textData.common).map((i) => Number(i));

      return data;
      /*  return {
        x:this.parseTextData(this.textData[this.visibleSet]).map((i) =>
        Number(i),
        y:
      )
      }; */
    },
  },
  watch: {
    plotType() {
      this.kind = this.kinds[this.plotType][0].value;
    },
    kind() {
      this.visualize();
    },

    async sampleDatasetName() {
      const res = await this.getSampleDataset(this.sampleDatasetName);
      this.sampleDataset = await res.json();
    },
  },
  async mounted() {
    const res = await this.getSampleDataNames();
    this.sampleDatasetNames = await res.json();
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  font-size: 20px;
  margin-top: 60px;
}
</style>
