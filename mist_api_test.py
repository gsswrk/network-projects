---
- name: Test Mist API call with Ansible
  hosts: D2
  connection: network_cli
  gather_facts: no
  vars:
    org_id: abc123
  vars_prompt:
    - name: email
      prompt: What is your Mist email?
      private: no
    - name: password
      prompt: What is your Mist password?
      private: yes

  tasks:
    - name: GET json output from Mist API
      uri:
        url_username: "{{ email }}"
        url_password: "{{ password }}"
        method: GET
        force_basic_auth: yes
        url: https://api.mist.com/api/v1/orgs/{{ org_id }}/inventory?site_id=xyz987
      register: mist_out_json

    - name: Display all json output
      debug:
        var: mist_out_json
