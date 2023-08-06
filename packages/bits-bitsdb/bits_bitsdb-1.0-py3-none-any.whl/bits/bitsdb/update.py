"""BITSdb Update class file."""


class Update(object):
    """BITSDB Update class."""

    def __init__(self, bitsdb):
        """Initialize an Update class instance."""
        self.bitsdb = bitsdb
        self.verbose = bitsdb.verbose

    #
    # Accounts
    #
    def bitsdb_authorized_keys(self, accounts, bitsdb):
        """Update the authorized_keys collection in BITSdb."""
        # get authorized_keys from /home/unix
        print('Getting authorized_keys files from /home/unix...')
        authorized_keys = accounts.getAuthorizedKeys()
        print('Found %s authorized_keys files.' % (len(authorized_keys)))

        # get authorized_keys from BITSdb
        print('Getting authorized_keys from BITSdb...')
        bitsdb.getCollection('authorized_keys', authorized_keys)

        # update authorized_keys in BITSdb
        print('Updating authorized_keys in BITSdb...')
        bitsdb.updateCollection('authorized_keys', authorized_keys)

    def bitsdb_public_html(self, accounts, bitsdb):
        """Update the public_html collection in BITSdb."""
        # get public_html from /home/unix
        print('Getting public_html directories from /home/unix...')
        public_html = accounts.getPublicHtml()
        print('Found %s public_html directories.' % (len(public_html)))

        # get public_html from BITSdb
        print('Getting public_html from BITSdb...')
        bitsdb.getCollection('public_html', public_html)

        # update public_html in BITSdb
        print('Updating public_html in BITSdb...')
        bitsdb.updateCollection('public_html', public_html)

    #
    # Active Directory (AD)
    #
    def bitsdb_ad_users(self, ad, bitsdb):
        """Update the ad_users collection in BITSdb."""
        # get users from AD
        print('Getting users from AD...')
        ad_users = ad.getUsers(attrlist=ad.user_attributes, full=False)
        print('Found %s users in AD.' % (len(ad_users)))

        # get ad_users from BITSdb
        print('Getting ad_users from BITSdb...')
        bitsdb.getCollection('ad_users', ad_users)

        # update ad_users in BITSdb
        print('Updating ad_users in BITSdb...')
        bitsdb.updateCollection('ad_users', ad_users)

    def bitsdb_ad_groups(self, ad, bitsdb):
        """Update the ad_groups collection in BITSdb."""
        # get users from AD
        print('Getting groups from AD...')
        ad_groups = ad.getGroups()
        print('Found %s groups in AD.' % (len(ad_groups)))

        # get ad_users from BITSdb
        print('Getting ad_groups from BITSdb...')
        bitsdb.getCollection('ad_groups', ad_groups)

        # update ad_users in BITSdb
        print('Updating ad_groups in BITSdb...')
        bitsdb.updateCollection('ad_groups', ad_groups)

    #
    # Backupify
    #
    def bitsdb_backupify_users(self, backupify, bitsdb):
        """Update the backupify_users collection in BITSdb."""
        # get backupify_users from backupify api
        print('Getting users from Backupify API...')
        backupify_users = backupify.get_users_dict()
        print('Found %s backupify users.' % (len(backupify_users)))

        # get backupify_users from BITSdb
        print('Getting backupify_users from BITSdb...')
        bitsdb.getCollection('backupify_users', backupify_users)

        print('Updating backupify_users in BITSdb...')
        bitsdb.updateCollection('backupify_users', backupify_users)

    #
    # Calendar
    #
    def bitsdb_scientific_calendars(self, calendar, bitsdb):
        """Update the scientific_calendars collection in BITSdb."""
        # get scientific_calendars from calendar db
        print('Getting calendars from Calendar MySQL DB...')
        scientific_calendars = calendar.getScientificCalendars()
        print('Found %s scientific calendars.' % (len(scientific_calendars)))

        # get scientific_calendars from BITSdb
        print('Getting scientific_calendars from BITSdb...')
        bitsdb.getCollection('scientific_calendars', scientific_calendars)

        print('Updating scientific_calendars in BITSdb...')
        bitsdb.updateCollection('scientific_calendars', scientific_calendars)

    #
    # Casper
    #
    def bitsdb_casper_computers(self, casper, bitsdb):
        """Update the casper_computers collection in BITSdb."""
        # get computers from casper db
        print('Getting computers from Casper MySQL DB...')
        casper_computers = casper.getComputers()
        print('Found %s casper computers.' % (len(casper_computers)))

        # get casper_computers from BITSdb
        print('Getting casper_computers from BITSdb...')
        bitsdb.getCollection('casper_computers', casper_computers)

        print('Updating casper_computers in BITSdb...')
        bitsdb.updateCollection('casper_computers', casper_computers)

    #
    # CCURE
    #
    def bitsdb_ccure_cards(self, ccure, bitsdb, env=''):
        """Update ccure_cards in BITSdb."""
        # get credentials from ccure db
        print('Getting cards (Credentials) from CCURE%s DB...' % env)
        ccure_cards = ccure.getCredentials()
        print('Found %s ccure cards.' % (len(ccure_cards)))

        # get ccure cards from BITSdb
        print('Getting ccure%s_cards from BITSdb...' % env)
        bitsdb.getCollection('ccure%s_cards' % env, ccure_cards)

        # update ccure card in BITSdb
        print('Updating ccure%s_cards in BITSdb...' % env)
        bitsdb.updateCollection('ccure%s_cards' % env, ccure_cards)

    def bitsdb_ccure_people(self, ccure, bitsdb, env=''):
        """Update ccure_people in BITSdb."""
        # get personnel from ccure db
        print('Getting people (Personnel) from CCURE%s DB...' % env)
        ccure_people = ccure.getPersonnel()
        print('Found %s ccure people.' % (len(ccure_people)))

        # get ccure people from BITSdb
        print('Getting ccure%s_people from BITSdb...' % env)
        bitsdb.getCollection('ccure%s_people' % env, ccure_people)

        # update ccure people in BITSdb
        print('Updating ccure%s_people in BITSdb...' % env)
        bitsdb.updateCollection('ccure%s_people' % env, ccure_people)

    def bitsdb_ccure_personnel_types(self, ccure, bitsdb, env=''):
        """Update ccure_personnel_types in BITSdb."""
        # get personnel types from ccure db
        print('Getting personnel_types (Personnal Types) from CCURE%s DB...' % env)
        ccure_personnel_types = ccure.getPersonnelTypes()
        print('Found %s ccure personnel_types.' % (len(ccure_personnel_types)))

        # get ccure personnel_types from BITSdb
        print('Getting ccure%s_personnel_types from BITSdb...' % env)
        bitsdb.getCollection(
            'ccure%s_personnel_types' % env,
            ccure_personnel_types
        )

        # update ccure personnel_types in BITSdb
        print('Updating ccure%s_personnel_types in BITSdb...' % env)
        bitsdb.updateCollection(
            'ccure%s_personnel_types' % env,
            ccure_personnel_types
        )

    #
    # DHCP
    #

    #
    # Disclosure
    #
    def bitsdb_disclosure_people(self, disclosure, bitsdb):
        """Update disclosure_people collection in BITSdb."""
        # get people from disclosure db
        print('Getting people from Disclosure MongoDB...')
        disclosure_people = disclosure.getPeople()
        print('Found %s disclosure people.' % (len(disclosure_people)))

        # get people from BITSdb
        print('Getting disclosure_people from BITSdb...')
        bitsdb.getCollection('disclosure_people', disclosure_people)

        # update people in BITSdb
        print('Updating disclosure_people in BITSdb...')
        bitsdb.updateCollection('disclosure_people', disclosure_people)

    def bitsdb_disclosure_users(self, disclosure, bitsdb):
        """Update disclosure_users collection in BITSdb."""
        # get users from disclosure db
        print('Getting users from Disclosure MongoDB...')
        disclosure_users = disclosure.getUsers()
        print('Found %s disclosure users.' % (len(disclosure_users)))

        # get users from BITSdb
        print('Getting disclosure_users from BITSdb...')
        bitsdb.getCollection('disclosure_users', disclosure_users)

        # update users in BITSdb
        print('Updating disclosure_users in BITSdb...')
        bitsdb.updateCollection('disclosure_users', disclosure_users)

    #
    # GitHub
    #
    def bitsdb_github_collaborators(self, github, bitsdb):
        """Update github_collaborators collection in BITSdb."""
        # get collaborators from github
        print('Getting all collaborators from GitHub...')
        github_collaborators = github.getCollaborators()
        print('Found %s github collaborators.' % (len(github_collaborators)))

        # get collaborators from BITSdb
        print('Getting github_collaborators from BITSdb...')
        bitsdb.getCollection('github_collaborators', github_collaborators)

        # update collaborators in BITSdb
        print('Updating github_collaborators in BITSdb...')
        bitsdb.updateCollection('github_collaborators', github_collaborators)

    def bitsdb_github_collaborators_repos(self, github, bitsdb):
        """Update github_collaborators_repos collection in BITSdb."""
        # get collaborators and their repos from github
        print('Getting all collaborators and their repos from GitHub...')
        github_collaborators = github.getCollaboratorsRepos()
        print('Found %s github collaborators w/repos.' % (len(github_collaborators)))

        # get collaborators from BITSdb
        print('Getting github_collaborators_repos from BITSdb...')
        bitsdb.getCollection('github_collaborators_repos', github_collaborators)

        # update collaborators in BITSdb
        print('Updating github_collaborators_repos in BITSdb...')
        bitsdb.updateCollection('github_collaborators_repos', github_collaborators)

    def bitsdb_github_members(self, github, bitsdb):
        """Update github_members collection in BITSdb."""
        # get members from github
        print('Getting organization members from GitHub...')
        github_members = github.getOrgMembers()
        print('Found %s github org members.' % (len(github_members)))

        # get github_members from BITSdb
        print('Getting github_members from BITSdb...')
        bitsdb.getCollection('github_members', github_members)

        # update github_members in BITSdb
        print('Updating github_members in BITSdb...')
        bitsdb.updateCollection('github_members', github_members)

    def bitsdb_github_users(self, github, bitsdb):
        """Update github_users collection in BITSdb."""
        # get members from bitsdb
        print('Getting initial github_users from BITSdb...')
        bitsdb_users = bitsdb.getCollection('github_users')

        # get members from github
        print('Updating member data from GitHub...')
        github_users = github.updateOrgMembers(bitsdb_users)
        print('Found %s github members.' % (len(github_users)))

        # get members from BITSdb
        print('Getting github_users from BITSdb...')
        bitsdb.getCollection('github_users', github_users)

        # update members in BITSdb
        print('Updating github_users in BITSdb...')
        bitsdb.updateCollection('github_users', github_users)

    def bitsdb_github_repos(self, github, bitsdb):
        """Update github_repos collection in BITSdb."""
        # get repos from BITSdb
        print('Getting initial github_repos from BITSdb...')
        bitsdb_repos = bitsdb.getCollection('github_repos')

        # get repos from github
        print('Updating repos data from GitHub...')
        github_repos = github.updateOrgRepos(bitsdb_repos)
        print('Found %s github repos.' % (len(github_repos)))

        # get repos from BITSdb
        print('Getting github_repos from BITSdb...')
        bitsdb.getCollection('github_repos', github_repos)

        # update repos in BITSdb
        print('Updating github_repos in BITSdb...')
        bitsdb.updateCollection('github_repos', github_repos)

    def bitsdb_github_repos_collaborators(self, github, bitsdb):
        """Update github_repos_collaborators collection in BITSdb."""
        # get repos from github
        print('Getting all repos and their collaborators from GitHub...')
        github_repos = github.getReposCollaborators()
        print('Found %s github repos w/collabroators.' % (len(github_repos)))

        # get repos from BITSdb
        print('Getting github_repos_collaborators from BITSdb...')
        bitsdb.getCollection('github_repos_collaborators', github_repos)

        # update repos in BITSdb
        print('Updating github_repos_collaborators in BITSdb...')
        bitsdb.updateCollection('github_repos_collaborators', github_repos)

    def bitsdb_github_teams(self, github, bitsdb):
        """Update github_teams collection in BITSdb."""
        # get teams from github
        print('Getting initial github_teams from BITSdb...')
        bitsdb_teams = bitsdb.getCollection('github_teams')

        print('Updating teams data from GitHub...')
        github_teams = github.updateOrgTeams(bitsdb_teams)
        print('Found %s github teams.' % (len(github_teams)))

        # # get members for each team
        # print('Getting all team members from GitHub...')
        # github_teams = github.getTeamsWithMembers()
        #
        # # get repos for each team
        # print('Getting all team repos from GitHub...')
        # github_teams = github.getTeamsWithRepos()

        # get teams from BITSdb
        print('Getting github_teams from BITSdb...')
        bitsdb.getCollection('github_teams', github_teams)

        # update teams in BITSdb
        print('Updating github_teams in BITSdb...')
        bitsdb.updateCollection('github_teams', github_teams)

    #
    # Google
    #
    def bitsdb_google_billing_accounts(self, g, bitsdb):
        """Update google_billing_accounts in BITSdb."""
        # get all billing accounts from google API
        print('Getting Google Billing Accounts from the Cloud Billing API...')
        billing_accounts = g.getBillingAccounts(projects=True, iampolicy=True)
        print('Found %s google billing accounts.' % (len(billing_accounts)))

        # get billing accounts from MongoDB
        print('Getting google_billing_accounts from BITSdb...')
        bitsdb.getCollection('google_billing_accounts', billing_accounts)

        # update billing accounts in MongoDB
        print('Updating google_billing_accounts in BITSdb...')
        bitsdb.updateCollection('google_billing_accounts', billing_accounts)

    def bitsdb_google_calendars(self, g, bitsdb):
        """Update google_calendars in BITSdb."""
        # get all calendars from google API
        print('Getting all calendars from Google...')
        google_calendars = g.getAllCalendars()
        print('Found %s google calendars.' % (len(google_calendars)))

        # get calendars from MongoDB
        print('Getting google_calendars from BITSdb...')
        bitsdb.getCollection('google_calendars', google_calendars)

        # update calendars in MongoDB
        print('Updating google_calendars in BITSdb...')
        bitsdb.updateCollection('google_calendars', google_calendars)

    def bitsdb_google_folders(self, g, bitsdb):
        """Update google_folders in BITSdb."""
        g.auth_service_account(g.scopes, g.subject)

        # get all folderfolders from google API
        print('Getting Google folders from the Cloud Resource Manager API...')
        google_folders = g.crm().get_organizations_folders()
        print('Found %s google folders.' % (len(google_folders)))

        # get folders from MongoDB
        print('Getting google_folders from BITSdb...')
        bitsdb.getCollection('google_folders', google_folders)

        # update folders in MongoDB
        print('Updating google_folders in BITSdb...')
        bitsdb.updateCollection('google_folders', google_folders)

    def bitsdb_google_email_forwarding(self, g, bitsdb):
        """Update google_email_forwarding in BITSdb."""
        # g.auth_service_account(g.scopes, g.subject)

        # get all forwarding settings from google API
        print('Getting all email forwarding settings from Google...')
        google_email_forwarding = g.getEmailForwardingSettings()
        print('Found %s google email forwarding settings.' % (len(google_email_forwarding)))

        # get users from MongoDB
        print('Getting google_email_forwarding from BITSdb...')
        bitsdb.getCollection('google_email_forwarding', google_email_forwarding)

        # update users in MongoDB
        print('Updating google_email_forwarding in BITSdb...')
        bitsdb.updateCollection('google_email_forwarding', google_email_forwarding)

    def bitsdb_google_groups(self, g, bitsdb):
        """Update google_groups in BITSdb."""
        g.auth_service_account(g.scopes, g.subject)

        # get all groups from google API
        print('Getting all groups from Google...')
        google_groups = g.directory().get_groups_dict()
        print('Found %s google groups.' % (len(google_groups)))

        # get groups from MongoDB
        print('Getting google_groups from BITSdb...')
        bitsdb.getCollection('google_groups', google_groups)

        # update groups in MongoDB
        print('Updating google_groups in BITSdb...')
        bitsdb.updateCollection('google_groups', google_groups)

    def bitsdb_google_groups_by_member(self, g, bitsdb):
        """Update google_groups_by_member in BITSdb."""
        # get all groups from google API
        print('Getting Google Users and Groups from BITSdb...')
        bitsdb_users = bitsdb.getCollection('google_users')
        bitsdb_groups = bitsdb.getCollection('google_groups_with_members')
        google_groups_by_member = g.getGroupsByMember(
            bitsdb_groups,
            bitsdb_users,
        )
        print('Found %s google group members.' % (len(google_groups_by_member)))

        # get google_groups_by_member from MongoDB
        print('Getting google_groups_by_member from BITSdb...')
        bitsdb.getCollection('google_groups_by_member', google_groups_by_member)

        # update google_groups_by_member in MongoDB
        print('Updating google_groups_by_member in BITSdb...')
        bitsdb.updateCollection('google_groups_by_member', google_groups_by_member)

    def bitsdb_google_groups_settings(self, g, bitsdb):
        """Update google_groups_settings in BITSdb."""
        # get all groups_settings from google API
        print('Getting settings for all groups from Google...')
        google_groups_settings = g.getAllGroupsSettings()
        print('Found settings for %s groups.' % (len(google_groups_settings)))

        # get google_groups_settings from MongoDB
        print('Getting google_groups_settings from BITSdb...')
        bitsdb.getCollection('google_groups_settings', google_groups_settings)

        # update google_groups_settings in MongoDB
        print('Updating google_groups_settings in BITSdb...')
        bitsdb.updateCollection('google_groups_settings', google_groups_settings)

    def bitsdb_google_organizations(self, g, bitsdb):
        """Update google_organizations in BITSdb."""
        g.auth_service_account(g.scopes, g.subject)

        # get all organizationorganizations from google API
        print('Getting Google organizations from the Cloud Resource Manager API...')
        google_organizations = g.crm().get_organizations_iampolicy()
        print('Found %s google organizations.' % (len(google_organizations)))

        # get organizations from MongoDB
        print('Getting google_organizations from BITSdb...')
        bitsdb.getCollection('google_organizations', google_organizations)

        # update organizations in MongoDB
        print('Updating google_organizations in BITSdb...')
        bitsdb.updateCollection('google_organizations', google_organizations)

    def bitsdb_google_people(self, g, bitsdb):
        """Update google_people in BITSdb."""
        # get all people from google API
        print('Getting Google People from the Google API...')
        google_people = g.getPeople()
        print('Found %s google people.' % (len(google_people)))

        # get people from MongoDB
        print('Getting google_people from BITSdb...')
        bitsdb.getCollection('google_people', google_people)

        # update people in MongoDB
        print('Updating google_people in BITSdb...')
        bitsdb.updateCollection('google_people', google_people)

    def bitsdb_google_projects(self, g, bitsdb):
        """Update google_projects in BITSdb."""
        # get all projects from google API
        print('Getting Google Projects from the Cloud Resource Manager API...')
        google_projects = g.getProjects()
        print('Found %s google projects.' % (len(google_projects)))

        # get projects from MongoDB
        print('Getting google_projects from BITSdb...')
        bitsdb.getCollection('google_projects', google_projects)

        # update projects in MongoDB
        print('Updating google_projects in BITSdb...')
        bitsdb.updateCollection('google_projects', google_projects)

    def bitsdb_google_projects_billinginfo(self, g, bitsdb):
        """Update google_projects_billinginfo in BITSdb."""
        g.auth_service_account(g.scopes, g.subject)

        # get all projects from google API
        print('Getting Google Projects from the Cloud Resource Manager API...')
        google_projects = g.crm().get_projects_dict()
        print('Found %s google projects.' % (len(google_projects)))

        # get all billing accounts from google API
        print('Getting Google Billing Accounts from Cloud Billing API...')
        billing_accounts = g.billing().get_billing_accounts()
        print('Found %s google billing accounts.' % (len(billing_accounts)))

        # # get projects_billinginfo from MongoDB
        # print('Getting google_project_billinginfo from BITSdb...'
        # bitsdb.getCollection('google_project_billinginfo', google_project_billinginfo)

        # # update google_project_billinginfo in MongoDB
        # print('Updating google_project_billinginfo in BITSdb...'
        # bitsdb.updateCollection('google_project_billinginfo', google_project_billinginfo)

    def bitsdb_google_resources(self, g, bitsdb):
        """Update google_resources in BITSdb."""
        g.auth_service_account(g.scopes, g.subject)

        # get all resources from google API
        print('Getting all resources from Google...')
        google_resources = g.directory().get_resource_calendars_dict()
        print('Found %s google resource calendars.' % (len(google_resources)))

        # get resources from BITSdb
        print('Getting google_resources from BITSdb...')
        bitsdb.getCollection('google_resources', google_resources)

        # update resources in BITSdb
        print('Updating google_resources in BITSdb...')
        bitsdb.updateCollection('google_resources', google_resources)

    def bitsdb_google_service_accounts(self, g, bitsdb):
        """Update google_service_accounts in BITSdb."""
        # g.auth_service_account(g.scopes, g.subject)

        # get all service_accounts from google API
        print('Getting all service_accounts from Google...')
        google_service_accounts = g.getAllServiceAccounts()
        print('Found %s google service accounts.' % (len(google_service_accounts)))

        # get service_accounts from BITSdb
        print('Getting google_service_accounts from BITSdb...')
        bitsdb.getCollection('google_service_accounts', google_service_accounts)

        # update service_accounts in BITSdb
        print('Updating google_service_accounts in BITSdb...')
        bitsdb.updateCollection('google_service_accounts', google_service_accounts)

    def bitsdb_google_users(self, g, bitsdb):
        """Update google_users in BITSdb."""
        # g.auth_service_account(g.scopes, g.subject)

        # get all users from google API
        print('Getting all users from Google...')
        # google_users = g.directory().get_users_dict()
        google_users = g.getUsers()
        print('Found %s google users.' % (len(google_users)))

        # get users from BITSdb
        print('Getting google_users from BITSdb...')
        bitsdb.getCollection('google_users', google_users)

        # update users in BITSdb
        print('Updating google_users in BITSdb...')
        bitsdb.updateCollection('google_users', google_users)

    #
    # NIS
    #
    def bitsdb_nis_groups(self, nis, bitsdb):
        """Update nis_groups collection in BITSdb."""
        # get group map from NIS
        print('Getting group map from NIS...')
        nis_groups = nis.getGroup()
        print('Found %s nis groups.' % (len(nis_groups)))

        # get nis_groups from BITSdb
        print('Getting nis_groups from BITSdb...')
        bitsdb.getCollection('nis_groups', nis_groups)

        # update nis_groups in BITSdb
        print('Updating nis_groups in BITSdb...')
        bitsdb.updateCollection('nis_groups', nis_groups)

    def bitsdb_nis_mounts(self, nis, bitsdb):
        """Update nis_mounts collection in BITSdb."""
        # get mounts.byname from nis
        print('Getting mounts.byname map from NIS...')
        nis_mounts = nis.getMounts()
        print('Found %s nis mounts.' % (len(nis_mounts)))

        # get nis_mounts from BITSdb
        print('Getting nis_mounts from BITSdb...')
        bitsdb.getCollection('nis_mounts', nis_mounts)

        # update nis_mounts in BITSdb
        print('Updating nis_mounts in BITSdb...')
        bitsdb.updateCollection('nis_mounts', nis_mounts)

    def bitsdb_nis_users(self, nis, bitsdb):
        """Update nis_users collection in BITSdb."""
        # get passwd map from nis
        print('Getting passwd map from NIS...')
        nis_users = nis.getPasswd()
        print('Found %s nis users.' % (len(nis_users)))

        # get nis_users from BITSdb
        print('Getting nis_users from BITSdb...')
        bitsdb.getCollection('nis_users', nis_users)

        # update nis_users in BITSdb
        print('Updating nis_users in BITSdb...')
        bitsdb.updateCollection('nis_users', nis_users)

    #
    # People
    #
    def bitsdb_people(self, people, bitsdb):
        """Update people collection in BITSdb."""
        # get people from People MySQL DB
        print('Getting people from People...')
        people_people = people.getPeople()
        print('Found %s people.' % (len(people_people)))

        # get people from BITSdb
        print('Getting people from BITSdb...')
        bitsdb.getCollection('people', people_people)

        # update people in BITSdb
        print('Updating people in BITSdb...')
        bitsdb.updateCollection('people', people_people)

    def bitsdb_people_users(self, people, bitsdb):
        """Update people collection in BITSdb."""
        # get users from People MySQL DB
        print('Getting users from People...')
        people_users = people.getUsers()
        print('Found %s people users.' % (len(people_users)))

        # get people from BITSdb
        print('Getting people_users from BITSdb...')
        bitsdb.getCollection('people_users', people_users)

        # update people in BITSdb
        print('Updating people_users in BITSdb...')
        bitsdb.updateCollection('people_users', people_users)

    def bitsdb_people_vendors(self, people, bitsdb):
        """Update people collection in BITSdb."""
        # get people from People MySQL DB
        print('Getting vendors from People...')
        people_vendors = people.getVendors()

        for vendor in people_vendors:
            collection = 'vendor_%s' % (vendor)
            vars()[collection] = people.getVendorData(vendor)
            print('Found %s %s vendor records in People.' % (
                len(vars()[collection]),
                vendor
            ))

            # get collection from BITSdb
            print('Getting %s from BITSdb...' % (collection))
            bitsdb.getCollection(collection, eval(collection))

            # update people in BITSdb
            print('Updating %s in BITSdb...' % (collection))
            bitsdb.updateCollection(collection, eval(collection))

    #
    # Pivotal Tracker
    #
    def bitsdb_pivotaltracker_projects(self, pivotaltracker, bitsdb):
        """Update pivotaltracker_projects in BITSdb."""
        # get projects from pivotal tracker api
        print('Getting all projects from Pivotal Tracker...')
        pivotaltracker_projects = pivotaltracker.getProjects()
        print('Found %s pivotaltracker projects.' % (len(pivotaltracker_projects)))

        print('Getting all projects from BITSdb...')
        bitsdb.getCollection('pivotaltracker_projects', pivotaltracker_projects)

        print('Updating projects in BITSdb...')
        bitsdb.updateCollection('pivotaltracker_projects', pivotaltracker_projects)

    #
    # Shoretel
    #
    def bitsdb_shoretel_phones(self, shoretel, bitsdb):
        """Update shoretel_phones collection in BITSdb."""
        # get phones from shoretel db
        print('Getting phones from ShoreTel DB...')
        shoretel_phones = shoretel.getPhones()
        print('Found %s shoretel phones.' % (len(shoretel_phones)))

        # get shoretel_phones from BITSdb
        print('Getting shoretel_phones from BITSdb...')
        bitsdb.getCollection('shoretel_phones', shoretel_phones)

        # update shoretel_phones in BITSdb
        print('Updating shoretel_phones in BITSdb...')
        bitsdb.updateCollection('shoretel_phones', shoretel_phones)

    #
    # Slack
    #
    def bitsdb_slack_channels(self, slack, bitsdb):
        """Update slack_channels collection in BITSdb."""
        # get users from slack api
        print('Getting channels from Slack API...')
        slack_channels = slack.get_channels()
        print('Found %s slack channels.' % (len(slack_channels)))

        # get slack_channels from BITSdb
        print('Getting slack_channels from BITSdb...')
        bitsdb.getCollection('slack_channels', slack_channels)

        # update slack_channels in BITSdb
        print('Updating slack_channels in BITSdb...')
        bitsdb.updateCollection('slack_channels', slack_channels)

    def bitsdb_slack_groups(self, slack, bitsdb):
        """Update slack_groups collection in BITSdb."""
        # get groups from slack api
        print('Getting groups from Slack API...')
        slack_groups = slack.get_groups()
        print('Found %s slack groups.' % (len(slack_groups)))

        # get slack_groups from BITSdb
        print('Getting slack_groups from BITSdb...')
        bitsdb.getCollection('slack_groups', slack_groups)

        # update slack_groups in BITSdb
        print('Updating slack_groups in BITSdb...')
        bitsdb.updateCollection('slack_groups', slack_groups)

    def bitsdb_slack_usergroups(self, slack, bitsdb):
        """Update slack_usergroups collection in BITSdb."""
        # get usergroups from slack api
        print('Getting usergroups from Slack API...')
        slack_usergroups = slack.get_usergroups()
        print('Found %s slack usergroups.' % (len(slack_usergroups)))

        # get slack_usergroups from BITSdb
        print('Getting slack_usergroups from BITSdb...')
        bitsdb.getCollection('slack_usergroups', slack_usergroups)

        # update slack_usergroups in BITSdb
        print('Updating slack_usergroups in BITSdb...')
        bitsdb.updateCollection('slack_usergroups', slack_usergroups)

    def bitsdb_slack_users(self, slack, bitsdb):
        """Update slack_users collection in BITSdb."""
        # get users from slack api
        print('Getting users from Slack API...')
        slack_users = slack.get_users()
        print('Found %s slack users.' % (len(slack_users)))

        # get slack_users from BITSdb
        print('Getting slack_users from BITSdb...')
        bitsdb.getCollection('slack_users', slack_users)

        # update slack_users in BITSdb
        print('Updating slack_users in BITSdb...')
        bitsdb.updateCollection('slack_users', slack_users)

    #
    # Space
    #
    def bitsdb_space_buildings(self, space, bitsdb):
        """Update space_buildings collection in BITSdb."""
        # get buildings from space
        print('Getting buildings from Space API...')
        space_buildings = space.getBuildings()
        print('Found %s space buildings.' % (len(space_buildings)))

        # get buildings from BITSdb
        print('Getting space_buildings from BITSdb...')
        bitsdb.getCollection('space_buildings', space_buildings)

        # update buildings in BITSdb
        print('Updating space_buildings in BITSdb...')
        bitsdb.updateCollection('space_buildings', space_buildings)

    def bitsdb_space_rooms(self, space, bitsdb):
        """Update space_rooms collection in BITSdb."""
        # get rooms from space
        print('Getting rooms from Space API...')
        space_rooms = space.getRooms()
        print('Found %s space rooms.' % (len(space_rooms)))

        # get rooms from BITSdb
        print('Getting space_rooms from BITSdb...')
        bitsdb.getCollection('space_rooms', space_rooms)

        # update rooms in BITSdb
        print('Updating space_rooms in BITSdb...')
        bitsdb.updateCollection('space_rooms', space_rooms)

    def bitsdb_space_desks(self, space, bitsdb):
        """Update space_desks collection in BITSdb."""
        # get desks from space
        print('Getting desks from Space API...')
        space_desks = space.getDesks()
        print('Found %s space desks.' % (len(space_desks)))

        # get desks from BITSdb
        print('Getting space_desks from BITSdb...')
        bitsdb.getCollection('space_desks', space_desks)

        # update desks in BITSdb
        print('Updating space_desks in BITSdb...')
        bitsdb.updateCollection('space_desks', space_desks)

    def bitsdb_space_seats(self, space, bitsdb):
        """Update space_seats collection in BITSdb."""
        # get seats from space
        print('Getting seats from Space API...')
        space_seats = space.getSeats()
        print('Found %s space seats.' % (len(space_seats)))

        # get seats from BITSdb
        print('Getting space_seats from BITSdb...')
        bitsdb.getCollection('space_seats', space_seats)

        # update seats in BITSdb
        print('Updating space_seats in BITSdb...')
        bitsdb.updateCollection('space_seats', space_seats)

    def bitsdb_space_users(self, space, bitsdb):
        """Update space_users collection in BITSdb."""
        # get users from space
        print('Getting users from Space API...')
        space_users = space.getUsers()
        print('Found %s space users.' % (len(space_users)))

        # get users from BITSdb
        print('Getting space_users from BITSdb...')
        bitsdb.getCollection('space_users', space_users)

        # update users in BITSdb
        print('Updating space_users in BITSdb...')
        bitsdb.updateCollection('space_users', space_users)

    #
    # Workday
    #
    def bitsdb_workday_people(self, workday, bitsdb):
        """Update the workday_people collection in BITSDB."""
        # get people from workday API
        print('Getting People people from Workday API...')
        workday_people = workday.find_dict()

        if workday_people:

            # get workday people new from BITSdb
            print('Getting workday_people from BITSdb...')
            bitsdb.getCollection('workday_people', workday_people)

            # update workday people in BITSdb
            print('Updating workday_people in BITSdb...')
            bitsdb.updateCollection('workday_people', workday_people)
