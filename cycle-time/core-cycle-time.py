#!/usr/bin/env python

import argparse
import os
import re
import subprocess
import sys
from datetime import datetime, timedelta

from dateutil.parser import parse as dateutil_parse


REPO_LIST = [
        "extensions/3D"
        ,"extensions/AbuseFilter"
        ,"extensions/ActiveAbstract"
        ,"extensions/AdvancedSearch"
        ,"extensions/AntiSpoof"
        ,"extensions/ApiFeatureUsage"
        ,"extensions/ArticleCreationWorkflow"
        ,"extensions/ArticlePlaceholder"
        ,"extensions/Babel"
        ,"extensions/BetaFeatures"
        ,"extensions/BounceHandler"
        ,"extensions/Calendar"
        ,"extensions/Campaigns"
        ,"extensions/Capiunto"
        ,"extensions/CategoryTree"
        ,"extensions/CentralAuth"
        ,"extensions/CentralNotice"
        ,"extensions/CharInsert"
        ,"extensions/CheckUser"
        ,"extensions/CirrusSearch"
        ,"extensions/Cite"
        ,"extensions/CiteThisPage"
        ,"extensions/Citoid"
        ,"extensions/cldr"
        ,"extensions/CodeEditor"
        ,"extensions/CodeMirror"
        ,"extensions/CodeReview"
        ,"extensions/Cognate"
        ,"extensions/CollaborationKit"
        ,"extensions/Collection"
        ,"extensions/CommonsMetadata"
        ,"extensions/ConfirmEdit"
        ,"extensions/CongressLookup"
        ,"extensions/ContactPage"
        ,"extensions/ContentTranslation"
        ,"extensions/ContributionTracking"
        ,"extensions/CreditsSource"
        ,"extensions/Dashiki"
        ,"extensions/Disambiguator"
        ,"extensions/DiscussionTools"
        ,"extensions/DismissableSiteNotice"
        ,"extensions/DonationInterface"
        ,"extensions/DoubleWiki"
        ,"extensions/DynamicSidebar"
        ,"extensions/Echo"
        ,"extensions/Elastica"
        ,"extensions/ElectronPdfService"
        ,"extensions/EntitySchema"
        ,"extensions/EventBus"
        ,"extensions/EventLogging"
        ,"extensions/EventStreamConfig"
        ,"extensions/ExtensionDistributor"
        ,"extensions/ExternalGuidance"
        ,"extensions/FeaturedFeeds"
        ,"extensions/FileExporter"
        ,"extensions/FileImporter"
        ,"extensions/FlaggedRevs"
        ,"extensions/Flow"
        ,"extensions/FundraiserLandingPage"
        ,"extensions/FundraisingTranslateWorkflow"
        ,"extensions/Gadgets"
        ,"extensions/GeoCrumbs"
        ,"extensions/GeoData"
        ,"extensions/GettingStarted"
        ,"extensions/GlobalBlocking"
        ,"extensions/GlobalCssJs"
        ,"extensions/GlobalPreferences"
        ,"extensions/GlobalUsage"
        ,"extensions/GlobalUserPage"
        ,"extensions/GoogleNewsSitemap"
        ,"extensions/Graph"
        ,"extensions/GrowthExperiments"
        ,"extensions/GuidedTour"
        ,"extensions/GWToolset"
        ,"extensions/ImageMap"
        ,"extensions/InputBox"
        ,"extensions/Insider"
        ,"extensions/intersection"
        ,"extensions/Interwiki"
        ,"extensions/InterwikiSorting"
        ,"extensions/Jade"
        ,"extensions/Josa"
        ,"extensions/JsonConfig"
        ,"extensions/Kartographer"
        ,"extensions/LabeledSectionTransclusion"
        ,"extensions/LandingCheck"
        ,"extensions/LdapAuthentication"
        ,"extensions/Linter"
        ,"extensions/LiquidThreads"
        ,"extensions/Listings"
        ,"extensions/LocalisationUpdate"
        ,"extensions/LoginNotify"
        ,"extensions/MachineVision"
        ,"extensions/MapSources"
        ,"extensions/MassMessage"
        ,"extensions/Math"
        ,"extensions/MobileApp"
        ,"extensions/MobileFrontend"
        ,"extensions/MultimediaViewer"
        ,"extensions/NavigationTiming"
        ,"extensions/Newsletter"
        ,"extensions/NewUserMessage"
        ,"extensions/Nuke"
        ,"extensions/OATHAuth"
        ,"extensions/OAuth"
        ,"extensions/OpenStackManager"
        ,"extensions/ORES"
        ,"extensions/PageAssessments"
        ,"extensions/PagedTiffHandler"
        ,"extensions/PageImages"
        ,"extensions/PageTriage"
        ,"extensions/PageViewInfo"
        ,"extensions/ParserFunctions"
        ,"extensions/ParsoidBatchAPI"
        ,"extensions/PdfHandler"
        ,"extensions/PerformanceInspector"
        ,"extensions/Petition"
        ,"extensions/Poem"
        ,"extensions/PoolCounter"
        ,"extensions/Popups"
        ,"extensions/ProofreadPage"
        ,"extensions/PropertySuggester"
        ,"extensions/QuickSurveys"
        ,"extensions/Quiz"
        ,"extensions/ReadingLists"
        ,"extensions/RelatedArticles"
        ,"extensions/Renameuser"
        ,"extensions/RevisionSlider"
        ,"extensions/RSS"
        ,"extensions/SandboxLink"
        ,"extensions/Score"
        ,"extensions/Scribunto"
        ,"extensions/SearchExtraNS"
        ,"extensions/SecureLinkFixer"
        ,"extensions/SecurePoll"
        ,"extensions/Sentry"
        ,"extensions/ShortUrl"
        ,"extensions/SiteMatrix"
        ,"extensions/SpamBlacklist"
        ,"extensions/SubPageList3"
        ,"extensions/SubpageSortkey"
        ,"extensions/SyntaxHighlight_GeSHi"
        ,"extensions/TemplateData"
        ,"extensions/TemplateSandbox"
        ,"extensions/TemplateStyles"
        ,"extensions/TemplateWizard"
        ,"extensions/TextExtracts"
        ,"extensions/Thanks"
        ,"extensions/TheWikipediaLibrary"
        ,"extensions/TimedMediaHandler"
        ,"extensions/timeline"
        ,"extensions/TitleBlacklist"
        ,"extensions/TocTree"
        ,"extensions/TorBlock"
        ,"extensions/Translate"
        ,"extensions/TranslationNotifications"
        ,"extensions/TrustedXFF"
        ,"extensions/TwoColConflict"
        ,"extensions/UniversalLanguageSelector"
        ,"extensions/UploadsLink"
        ,"extensions/UploadWizard"
        ,"extensions/UrlShortener"
        ,"extensions/UserMerge"
        ,"extensions/VipsScaler"
        ,"extensions/VisualEditor"
        ,"extensions/WebAuthn"
        ,"extensions/Wikibase"
        ,"extensions/WikibaseCirrusSearch"
        ,"extensions/WikibaseLexeme"
        ,"extensions/WikibaseLexemeCirrusSearch"
        ,"extensions/WikibaseMediaInfo"
        ,"extensions/WikibaseQualityConstraints"
        ,"extensions/Wikidata.org"
        ,"extensions/WikidataPageBanner"
        ,"extensions/WikiEditor"
        ,"extensions/wikihiero"
        ,"extensions/WikiLove"
        ,"extensions/WikimediaBadges"
        ,"extensions/WikimediaEditorTasks"
        ,"extensions/WikimediaEvents"
        ,"extensions/WikimediaIncubator"
        ,"extensions/WikimediaMaintenance"
        ,"extensions/WikimediaMessages"
        ,"extensions/Wikisource"
        ,"extensions/XAnalytics"
        ,"skins/CologneBlue"
        ,"skins/MinervaNeue"
        ,"skins/Modern"
        ,"skins/MonoBook"
        ,"skins/Nostalgia"
        ,"skins/Timeless"
        ,"skins/Vector"
        ,"vendor"]


# Messages we don't want to see in the git log
SKIP_MESSAGES = [
    'Localisation updates from',
    # Fix for escaping fail leaving a commit summary of $COMMITMSG
    'COMMITMSG',
    r'Add (\.gitreview( and )?)?\.gitignore',
    # Branching commit; set $wgVersion, defaultbranch, add submodules
    'Creating new WMF',
    'Updating development dependencies',
    # git submodule autobumps
    r'Updated mediawiki\/core',
]


def valid_change(log_message):
    """
    validates a change based on a commit
    """
    for skip_message in SKIP_MESSAGES:
        if re.search(skip_message, log_message):
            return False

    return True


def parse_args(args=None):
    """
    Parse args
    """
    ap = argparse.ArgumentParser()
    ap.add_argument('-C', '--core-path', required=True, help='Path to core checkout')
    ap.add_argument(
        '-w',
        '--wmf-version',
        dest='wmf_versions',
        action='append',
        required=True,
        help='wmf version'
    )
    return ap.parse_args()


def p95_time(git_logs, train_time):
    if not git_logs:
        return 0

    times = []
    for log in git_logs:
        log = log.split()
        log_message = log[:-1]
        log_epoch = log[-1]
        if not valid_change(' '.join(log_message)):
            continue
        times.append(train_time - int(log_epoch))

    times = sorted(times)
    return times[int(len(times) * 0.95)]


def format_seconds(seconds):
    """
    Human readable seconds

	<https://stackoverflow.com/a/4048773>
    """
    sec = timedelta(seconds=seconds)
    d = datetime(1, 1, 1) + sec

    return '%d:%d:%d:%d' % (d.day-1, d.hour, d.minute, d.second)


def previous_version(version, path):
    """
    Get the previous version for version numbers like 1.35.0-wmf.10
    """
    version = version.split('.')
    last_digit = int(version[-1]) - 1

    if last_digit <= 0:
        raise RuntimeError('I\'m too stupid for this shit')

    last_version = os.path.join('wmf', '.'.join(version[:-1] + [str(last_digit)]))
    if subprocess.check_output(['git', '-C', path, 'for-each-ref', os.path.join('refs', 'remotes', 'origin', last_version)]):
        return os.path.join('origin', last_version)
    else:
        raise RuntimeError('Last version "%s" not found', last_version)


def git_log(git_range, path='.'):
    """
    git log of changes between old version and the train branch point
    """
    return subprocess.check_output([
        'git',
        '-C',
        path,
        'log',
        '--no-merges',
        "--format=%s %ct",
        git_range], text=True).splitlines()


def main(args=None):
    args = parse_args(args)
    core_path = args.core_path
    versions = args.wmf_versions
    total_p95 = 0
    for version in versions:
        all_changes = []
        version_count = 0
        if ',' in version:
            old_version, version = version.split(',')
            old_version = os.path.join('origin', 'wmf', old_version)
        else:
            old_version = previous_version(version, core_path)

        for repo in ['.'] + REPO_LIST:
            path = os.path.join(core_path, repo)
            try:
                train_sha, train_time = subprocess.check_output(
                    ['git', '-C', path, 'log', '--format=%H %ct', '--reverse', 'origin/master..origin/wmf/{}'.format(version)],
                    text=True
                ).splitlines()[0].split()
            except:
                # This should fail for extensions since there is not extra commit for extensions
                if repo == '.':
                    raise

                train_sha = subprocess.check_output(
                    ['git', '-C', path, 'merge-base', 'origin/master', 'origin/wmf/{}'.format(version)],
                    text=True
                ).strip()

            train_time = int(train_time)
            git_range = '{}..{}'.format(str(old_version), str(train_sha))
            all_changes += git_log(git_range, path)
        p95 = p95_time(all_changes, train_time)
        total_p95 += p95
        print('{}\t{}'.format(version, format_seconds(p95)))

    print('Average for p95: {}'.format(format_seconds(int(total_p95/len(versions)))))


if __name__ == '__main__':
    main(sys.argv[1:])
