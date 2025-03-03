<script lang="ts">
  import Button from '$lib/components/Button.svelte';
  import DomainMetadataPanel from '$lib/components/authentication/DomainMetadataPanel.svelte';
  import Modal from '$lib/components/Modal.svelte';
  import Input from '$lib/components/Input.svelte';
  import { getClient } from '$lib/store';

  async function createUser(
    { email, password, confirm_password, fullName, organization, website },
    client
  ) {
    if (password.value !== confirm_password.value) {
      throw Error('Password and password confirmation mismatch');
    }

    let newUser = {
      email: email.value,
      password: password.value,
      password_verify: confirm_password.value,
      name: fullName.value,
      institution: organization.value,
      website: website.value
    };
    // Filter attributes that doesn't exist
    Object.keys(newUser).forEach((k) => newUser[k] == '' && delete newUser[k]);
    await client.register(newUser); // This will return a success message and the new user info
  }
</script>

<div class="flex flex-col xl:flex-row w-full h-full xl:justify-around items-center gap-12">
  {#await getClient() then client}
    {#await client.metadata then metadata}
      <DomainMetadataPanel {metadata} />
      <form class="contents" on:submit|preventDefault={(e) => createUser(e.target, client)}>
        <Modal>
          <div
            class="flex flex-shrink-0 justify-between p-4 pb-0 flex-nowrap w-full h-min"
            slot="header"
          >
            <span class="block text-center w-full">
              <p class="text-2xl font-bold text-gray-800">Apply for an account</p>
            </span>
          </div>
          <div class="contents" slot="body">
            <div class="w-full gap-6 flex">
              <Input label="Full name" id="fullName" placeholder="Jane Doe" required />
              <Input
                label="Company/Institution"
                id="organization"
                placeholder="OpenMined University"
              />
            </div>
            <Input label="Email" id="email" placeholder="info@openmined.org" required />
            <div class="w-full gap-6 flex">
              <Input type="password" label="Password" id="password" placeholder="******" required />
              <Input
                type="password"
                label="Confirm Password"
                id="confirm_password"
                placeholder="******"
                required
              />
            </div>
            <Input label="Website/Profile" id="website" placeholder="https://openmined.org" />
            <p class="text-center">
              Already have an account? Sign in <a href="/login">here</a>.
            </p>
          </div>
          <Button variant="secondary" slot="button-group">Sign up</Button>
        </Modal>
      </form>
    {/await}
  {/await}
</div>
