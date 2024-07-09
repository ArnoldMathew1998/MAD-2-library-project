<template>
    <div class="image">
        <div class="headline-and-subhead">
          <div class="read-with-us">Read with us</div>
          <div class="reading-a-book">
            Reading a book with us opens doors to new worlds, sparks the
            imagination, and unravels the mysteries of the universe, one page at
            a time.
          </div>
        </div>
      </div>
</template>

<style scoped>
.read-with-us {
  position: relative;
  line-height: 64px;
  font-weight: 600;
}
.reading-a-book {
  width: 482px;
  position: relative;
  font-size: 24px;
  text-align: left;
  display: flex;
  align-items: center;
}
.headline-and-subhead,
.image {
  align-self: stretch;
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  justify-content: flex-start;
}
.headline-and-subhead {
  gap: 16px;
}
.image {
  background: linear-gradient(
    180deg,
    #edb294,
    #edb294 22%,
    #edb294 30%,
    #b2cbcf
  );
  overflow: hidden;
  padding: 400px 138px;
}



</style>