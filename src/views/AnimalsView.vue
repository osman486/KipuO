<template>

  <div class="container mt-4">

    <h1 class="mb-4">
      Животные
    </h1>

    <div
      class="card mb-3 shadow"
      v-for="animal in animals"
      :key="animal.id"
    >

      <div class="card-body">

        <h3>
          {{ animal.name }}
        </h3>

        <p>
          <strong>Тип:</strong>
          {{ animal.species }}
        </p>

        <p>
          <strong>Статус:</strong>
          {{ animal.rarity }}
        </p>

        <p>
          {{ animal.description }}
        </p>

      </div>

    </div>

  </div>

</template>

<script>

export default {

  data() {

    return {
      animals: []
    }

  },

  mounted() {

    fetch('http://127.0.0.1:5000/animals')

      .then(response => response.json())

      .then(data => {

        this.animals = data

      })

  }

}

</script>