<template>
  <div class="panel-body table-responsive">
    <table
      class="table table-striped table-sm"
      v-for="(category, name, index) in this.$store.translation"
      :key="index"
    >
      <thead class="thead-dark">
        <tr>
          <th scope="col">{{ name }}</th>
          <th scope="col"></th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(translation, index) in category" :key="index">
          <td style="width: 50%">{{ translation.en }}</td>
          <td style="width: 50%">{{ translation.de }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<style>
.table-responsive {
  max-height:60vh;
}
</style>
