<template>
            <div class="row clearfix p-1">
              <div class="col-md-12 col-lg-4 clearfix">
                <q-card>
                  <q-card-title class="bg-primary">
                    <b>Current Semester</b>
                  </q-card-title>
                  <q-card-main class="card-block pt-2">
                    <q-list no-border>
                      <q-item>
                        <q-item-main>
                          <q-item-tile label>CS1400 ONL Spring 18</q-item-tile>
                           <q-item-tile sublabel lines="2">
                              15/33 Students Have Responded
                          </q-item-tile>
                        </q-item-main>
                      </q-item>
                      <q-item>
                        <q-item-main>
                          <q-item-tile label>CS1410 WSD Spring 18 (this course is not being evaluated)</q-item-tile>
                          <q-item-tile sublabel lines="2">
                              No Students Have Responded
                          </q-item-tile>
                        </q-item-main>
                      </q-item>
                    </q-list>
                  </q-card-main>

                </q-card>
              </div>
              <div class="col-md-12 col-lg-4 clearfix">
                <q-card>
                  <q-card-title class="bg-primary">
                    <b>Previous Semesters</b>
                  </q-card-title>
                  <q-card-main class="card-block pt-2">
                     <q-list no-border>
                      <q-item>
                        <q-item-main>
                          <q-item-tile label><q-btn @click="$refs.basicModal.open()">Fall 2017 (3 Courses)</q-btn></q-item-tile>
                        </q-item-main>
                      </q-item>
                      <q-item>
                        <q-item-main>
                          <q-item-tile label @click="$refs.basicModal2.open()"><q-btn>Summer 2017 (2 Courses)</q-btn></q-item-tile>
                        </q-item-main>
                      </q-item>
                    </q-list>
                  </q-card-main>
                </q-card>
              </div>

              <div class="col-md-12 col-lg-4 clearfix">
                <q-card>
                  <q-card-title class="bg-primary">
                    <b>Future Semesters</b>
                  </q-card-title>
                  <q-card-main class="card-block pt-2">
                     <q-list no-border>
                      <q-item>
                        <q-item-main>
                          <q-item-tile label><q-btn>Summer 2018 (3 Courses)</q-btn></q-item-tile>
                        </q-item-main>
                      </q-item>
                    </q-list>
                  </q-card-main>
                </q-card>
              </div>
              <q-modal ref="basicModal" :content-css="{padding: '50px'}">
                <h4>Fall 2017</h4>
                <q-list no-border>
                          <q-item>
                            <q-item-main>
                              <q-item-tile label>CS1400 ONL Fall 17</q-item-tile>
                               <q-item-tile sublabel lines="2">
                                  30/33 Students Have Responded
                              </q-item-tile>
                            </q-item-main>
                          </q-item>
                          <q-item>
                            <q-item-main>
                              <q-item-tile label>CS1410 WSD Fall 17 (this course is not being evaluated)</q-item-tile>
                              <q-item-tile sublabel lines="2">
                                  No Students Have Responded
                              </q-item-tile>
                            </q-item-main>
                          </q-item>
                        </q-list>
                <q-btn color="primary" @click="$refs.basicModal.close()">Close</q-btn>
              </q-modal>

              <q-modal ref="basicModal2" :content-css="{padding: '50px'}">
                <h4>Summer 2017</h4>
                <q-list no-border>
                          <q-item>
                            <q-item-main>
                              <q-item-tile label>CS1400 ONL Summer 17</q-item-tile>
                               <q-item-tile sublabel lines="2">
                                  30/33 Students Have Responded
                              </q-item-tile>
                            </q-item-main>
                          </q-item>
                          <q-item>
                            <q-item-main>
                              <q-item-tile label>CS1410 WSD Summer 17 (this course is not being evaluated)</q-item-tile>
                              <q-item-tile sublabel lines="2">
                                  No Students Have Responded
                              </q-item-tile>
                            </q-item-main>
                          </q-item>
                        </q-list>
                <q-btn color="primary" @click="$refs.basicModal2.close()">Close</q-btn>
              </q-modal>
            </div>
</template>
